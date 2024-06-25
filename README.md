# JPG to PNG Converter

This is a simple Python script that converts JPG images to PNG format.

## Installation

1. Clone the repository.
2. Install the required dependencies:
pip install -r requirements.txt

Copy
Insert

## Usage

1. Update the `config.json` file with the correct paths.
2. Run the script:
python jpg2png.py

Copy
Insert

## Configuration

The script uses a `config.json` file to specify the source and destination directories. The `config.json` file should contain the following:

```json
{
 "source_directory": "path_to_your_jpg_files",
 "destination_directory": "path_to_save_png_files"
}
How it works
The script reads the config.json file to determine the source and destination directories. It then iterates over all the files in the source directory, checking if they have a .jpg or .jpeg extension. For each file that meets this criteria, the script opens the image using the PIL library, saves it as a PNG file in the destination directory, and prints a message indicating the conversion was successful.

License
Apache 2.0 (https://choosealicense.com/licenses/apache-2.0/)
