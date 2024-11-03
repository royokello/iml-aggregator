import argparse
import os
import random
from PIL import Image

def main(
    input_dir: str,
    output_dir: str,
    resolution: int | None = None,
    mode: str = "folder"
):
    """
    Retrieves all image files and their captions from a specified directory and its subdirectories, converts them to PNG format,
    and saves them to a designated output folder with names as sequential integers.
    Modes:
    - folder: gathers files folder by folder and ordered as found
    - file: gathers files in order of filenames throughout the entire directory and subdirectories
    - random: gathers files in random order
    """
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Resolution: {resolution}")
    print(f"Mode: {mode}")

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Collect all image file paths based on the selected mode
    image_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
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
                # Convert the image to RGB mode if it's not already
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                if resolution:
                    original_width, original_height = img.size

                    # Determine orientation
                    if original_width > original_height:
                        # Landscape orientation
                        new_width = resolution
                        new_height = round(original_height * (resolution / original_width))
                    elif original_height > original_width:
                        # Portrait orientation
                        new_height = resolution
                        new_width = round(original_width * (resolution / original_height))
                    else:
                        # Square image
                        new_width, new_height = resolution, resolution

                    # Resize the image while maintaining aspect ratio
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Create a new square image with white background
                    new_img = Image.new('RGB', (resolution, resolution), (255, 255, 255))

                    # Calculate position to paste the resized image onto the white canvas
                    paste_x = (resolution - new_width) // 2
                    paste_y = (resolution - new_height) // 2

                    new_img.paste(resized_img, (paste_x, paste_y))
                else:
                    # If no resolution is provided, use the original image
                    new_img = img

                # Save the image
                output_file_path = os.path.join(output_dir, f"{file_counter}.png")
                new_img.save(output_file_path, "PNG")

                # Check for a caption file with the same name as the image
                caption_file_path = os.path.splitext(file_path)[0] + ".txt"
                if os.path.exists(caption_file_path):
                    with open(caption_file_path, "r") as caption_file:
                        caption_text = caption_file.read()
                        # Save the caption text to a corresponding output file
                        caption_output_path = os.path.join(output_dir, f"{file_counter}.txt")
                        with open(caption_output_path, "w") as output_caption_file:
                            output_caption_file.write(caption_text)

                print(f"Converted and saved: {output_file_path}")
                file_counter += 1

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect and convert images to PNG format.")
    parser.add_argument("-i", "--input_dir", type=str, required=True, help="Directory where the image files are located.")
    parser.add_argument("-o", "--output_dir", type=str, required=True, help="Directory where the PNG files will be saved.")
    parser.add_argument("-r", "--resolution", type=int, help="Maximum length for the longest side of the images. If not provided, resizing is skipped.")
    parser.add_argument("-m", "--mode", type=str, choices=["folder", "file", "random"], default="folder",
                        help="Mode to gather files: folder, file, or random.")

    args = parser.parse_args()
    main(args.input_dir, args.output_dir, args.resolution, args.mode)