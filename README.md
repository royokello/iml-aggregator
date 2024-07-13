# Image Aggregator
A Python script that retrieves all image files from a specified directory and its subdirectories, converts them to PNG format, and saves them to a designated output folder.

# Usage

To use this script, you need to have Python installed on your system along with the Pillow library. You can install Pillow using pip if it is not already installed:

\`\`\`bash
pip install Pillow
\`\`\`

Once Pillow is installed, you can run the script from the command line by specifying the source directory where the images are located and the output directory where the PNG files will be saved. Use the following command:

\`\`\`bash
python main.py --source_dir "path/to/source_directory" --output_dir "path/to/output_directory" --resolution 256
\`\`\`
