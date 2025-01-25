# Image Aggregator

A Python script that retrieves all image files from a specified directory and its subdirectories, converts them to PNG format, and saves them to a designated output folder. Additionally, the script collects any caption text files that share the same filename as the images.

## Usage

To use this script, you need to have Python installed on your system along with the Pillow library. You can install Pillow using pip if it is not already installed:

```bash
pip install Pillow
```

Once Pillow is installed, you can run the script from the command line by specifying:

- The **input** directory containing your image files.
- The **output** directory for the resulting PNG files.
- Optional **width** and **height** to resize the images:
  - If both are provided, the image is resized exactly to `width x height` (aspect ratio may change).
  - If only one dimension is provided, the other is scaled proportionally.
- Optional `--square` flag to place the final resized image on a white square background.
- A **mode** to specify how files are gathered (`folder`, `file`, or `random`).

Example command:

```bash
python image_converter.py \
    --input_dir "path/to/input_directory" \
    --output_dir "path/to/output_directory" \
    --width 256 \
    --height 256 \
    --square \
    --mode folder
```

## Arguments

- `-i`, `--input_dir`  
  Directory where the image files are located. **(Required)**

- `-o`, `--output_dir`  
  Directory where the PNG files (and any captions) will be saved. **(Required)**

- `--width`  
  Target width for the images. If only this is given, the height is scaled proportionally.

- `--height`  
  Target height for the images. If only this is given, the width is scaled proportionally.

- `--square`  
  If provided, the output image is placed on a square white background (side length is the larger of the final width/height).

- `-m`, `--mode`  
  Mode to gather files, with options:
  - **`folder`**: Gathers files in the order that `os.walk` returns them.  
  - **`file`**: Gathers files in alphabetical order by filename.  
  - **`random`**: Gathers files in a random order.

The script also looks for caption text files with the same names as the images (e.g., `image1.jpg` / `image1.txt`) and saves them in the output directory alongside the converted PNG files.

