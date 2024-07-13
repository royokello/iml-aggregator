import argparse
import os
from PIL import Image

def main(source_dir, output_dir, max_resolution=None):
    """
    Retrieves all image files from a specified directory and its subdirectories, converts them to PNG format, 
    and saves them to a designated output folder with names as sequential integers.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize a counter for the output file names
    file_counter = 1

    # Walk through all directories and files in the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                # Open the image file
                with Image.open(file_path) as img:

                    if max_resolution:
                        img.thumbnail((max_resolution, max_resolution), Image.LANCZOS)
                    # Construct the output file path with the counter
                    output_file_path = os.path.join(output_dir, f"{file_counter}.png")
                    # Convert to PNG and save in the output directory
                    # img.convert('RGBA').save(output_file_path, 'PNG')
                    img.save(output_file_path, 'PNG')
                    print(f"Converted and saved: {file_path} as {output_file_path}")
                    file_counter += 1  # Increment the file counter after successful conversion
            except IOError:
                # This catches files that are not images or are corrupted
                print(f"Failed to convert: {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect and convert images to PNG format.")
    parser.add_argument("-s", "--source_dir", type=str, required=True, help="Directory where the image files are located.")
    parser.add_argument("-o", "--output_dir", type=str, required=True, help="Directory where the PNG files will be saved.")
    parser.add_argument("-r", "--resolution", type=int, help="Optional maximum length for the longest side of the images.")

    args = parser.parse_args()
    main(args.source_dir, args.output_dir, args.resolution)