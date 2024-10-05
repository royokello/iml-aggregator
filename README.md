# Image Aggregator
A Python script that retrieves all image files from a specified directory and its subdirectories, converts them to PNG format, and saves them to a designated output folder. Additionally, the script collects available caption text files that share the same filename as the images.

# Usage

To use this script, you need to have Python installed on your system along with the Pillow library. You can install Pillow using pip if it is not already installed:

```
pip install Pillow
```

Once Pillow is installed, you can run the script from the command line by specifying the input directory where the images are located, the output directory where the PNG files will be saved, and additional options like resolution and mode. Use the following command:

```
python main.py -i "path/to/input_directory" -o "path/to/output_directory" -r 256 -m folder
```

# Arguments

- `-i`, `--input_dir`: Directory where the image files are located.
- `-o`, `--output_dir`: Directory where the PNG files and captions will be saved.
- `-r`, `--resolution`: Maximum length for the longest side of the images (e.g., 256).
- `-m`, `--mode`: Mode to gather files, with options:
  - `folder`: Gathers files folder by folder and ordered as found.
  - `file`: Gathers files in order of filenames throughout the entire directory and subdirectories.
  - `random`: Gathers files in random order.

The script also looks for caption text files with the same filenames as the images and saves them in the output directory.

