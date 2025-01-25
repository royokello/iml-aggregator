import argparse
import os
import random
from PIL import Image


def main(
    input_dir: str,
    output_dir: str,
    width: int | None = None,
    height: int | None = None,
    square: bool = False,
    mode: str = "folder"
):
    """
    Collects all image files (and their captions, if present) from a directory and its subdirectories, converts them to PNG,
    optionally resizes them according to the specified width and/or height, and saves the result.

    If both width and height are provided, the image is resized to exactly width x height (possibly changing the aspect ratio).

    If only one dimension is provided, the other is scaled proportionally to maintain the aspect ratio.

    If --square is provided, the final output image will be placed on a white square background whose side length is the larger
    dimension of the resized image (or the explicitly requested dimension if both are specified).\n\n    Modes:\n        - folder: gather files in folder order as returned by os.walk\n        - file: gather files sorted by filename\n        - random: gather files in random order\n    """
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Target width: {width}")
    print(f"Target height: {height}")
    print(f"Square output: {square}")
    print(f"Mode: {mode}")

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Collect all image file paths based on the selected mode
    image_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                image_files.append(os.path.join(root, file))

    if mode == "file":
        image_files.sort(key=lambda x: os.path.basename(x).lower())
    elif mode == "random":
        random.shuffle(image_files)
    # "folder" mode keeps the default order from os.walk

    # Initialize a counter for the output file names
    file_counter = 1

    for file_path in image_files:
        try:
            with Image.open(file_path) as img:
                # Convert the image to RGB if it's not already
                if img.mode != "RGB":
                    img = img.convert("RGB")

                original_width, original_height = img.size
                new_width, new_height = original_width, original_height

                # Determine new dimensions based on width and/or height
                if width is not None and height is not None:
                    # Directly resize to the specified width and height
                    new_width = width
                    new_height = height
                elif width is not None:
                    # Scale proportionally based on the provided width
                    ratio = width / original_width
                    new_width = width
                    new_height = int(original_height * ratio)
                elif height is not None:
                    # Scale proportionally based on the provided height
                    ratio = height / original_height
                    new_width = int(original_width * ratio)
                    new_height = height

                # Resize the image if we need to change dimensions
                if (new_width, new_height) != (original_width, original_height):
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # If square flag is enabled, place the resized image on a white square canvas
                if square:
                    # Determine the side of the square (largest dimension)
                    side = max(new_width, new_height)
                    square_img = Image.new("RGB", (side, side), (255, 255, 255))
                    paste_x = (side - new_width) // 2
                    paste_y = (side - new_height) // 2
                    square_img.paste(img, (paste_x, paste_y))
                    final_img = square_img
                else:
                    final_img = img

                # Save the final image
                output_file_path = os.path.join(output_dir, f"{file_counter}.png")
                final_img.save(output_file_path, "PNG")

                # Check for a caption file with the same name as the image
                caption_file_path = os.path.splitext(file_path)[0] + ".txt"
                if os.path.exists(caption_file_path):
                    with open(caption_file_path, "r", encoding="utf-8") as caption_file:
                        caption_text = caption_file.read()
                    caption_output_path = os.path.join(output_dir, f"{file_counter}.txt")
                    with open(caption_output_path, "w", encoding="utf-8") as output_caption_file:
                        output_caption_file.write(caption_text)

                print(f"Converted and saved: {output_file_path}")
                file_counter += 1

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect and convert images to PNG format.")
    parser.add_argument("-i", "--input_dir", type=str, required=True,
                        help="Directory where the image files are located.")
    parser.add_argument("-o", "--output_dir", type=str, required=True,
                        help="Directory where the PNG files will be saved.")
    parser.add_argument("--width", type=int,
                        help="Target width for the images. If only width is provided, the height is scaled proportionally.")
    parser.add_argument("--height", type=int,
                        help="Target height for the images. If only height is provided, the width is scaled proportionally.")
    parser.add_argument("--square", action="store_true",
                        help="If provided, output images are placed on a square white background.")
    parser.add_argument("-m", "--mode", type=str, choices=["folder", "file", "random"], default="folder",
                        help="Mode to gather files: folder, file, or random.")

    args = parser.parse_args()

    main(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        width=args.width,
        height=args.height,
        square=args.square,
        mode=args.mode
    )