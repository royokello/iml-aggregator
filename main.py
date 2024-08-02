import argparse
import os
from PIL import Image

def main(source_dir: str, output_dir: str, resolution: int):
    """
    Retrieves all image files from a specified directory and its subdirectories, converts them to PNG format, 
    and saves them to a designated output folder with names as sequential integers.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize a counter for the output file names
    file_counter = 1

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                with Image.open(file_path) as img:
                    # Convert the image to RGB mode if it's not already
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Resize the image to fit within the resolution while maintaining aspect ratio
                    img.thumbnail((resolution, resolution), Image.LANCZOS) # type: ignore

                    # Create a new square image with white background
                    new_img = Image.new('RGB', (resolution, resolution), (255, 255, 255))

                    # Calculate position to paste the original image
                    paste_position = ((resolution - img.width) // 2, (resolution - img.height) // 2)

                    # Paste the original image onto the new square image
                    new_img.paste(img, paste_position)

                    # Save the image
                    output_file_path = os.path.join(output_dir, f"{file_counter}.png")
                    new_img.save(output_file_path, "PNG")

                    print(f"Converted and saved: {output_file_path}")
                    file_counter += 1

            except Exception as e:
                print(f"Error processing {file}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect and convert images to PNG format.")
    parser.add_argument("-s", "--source_dir", type=str, required=True, help="Directory where the image files are located.")
    parser.add_argument("-o", "--output_dir", type=str, required=True, help="Directory where the PNG files will be saved.")
    parser.add_argument("-r", "--resolution", type=int, help="Optional maximum length for the longest side of the images.")

    args = parser.parse_args()
    main(args.source_dir, args.output_dir, args.resolution)