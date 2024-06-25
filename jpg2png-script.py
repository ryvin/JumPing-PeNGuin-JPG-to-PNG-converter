import os
import json
import logging
from PIL import Image
import sys
import imghdr
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def load_config():
    try:
        # Determine the path to the config file relative to the executable
        if getattr(sys, 'frozen', False):  # If running as a bundled executable
            application_path = Path(sys.executable).parent
        else:
            application_path = Path(__file__).parent

        config_file = application_path / 'config.json'
        with open(config_file, 'r') as file:
            config = json.load(file)

        # Validate config
        required_keys = ['source_directory', 'destination_directory']
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Missing required key in config: {key}")
            if not isinstance(config[key], str) or not config[key]:
                raise ValueError(f"Invalid value for {key} in config")

        return config
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as e:
        logging.error(f"Error loading config: {str(e)}")
        sys.exit(1)

def is_image(file_path):
    return imghdr.what(file_path) in ['jpeg', 'jpg']

def convert_image(source_path, dest_path):
    try:
        img = Image.open(source_path)
        img.save(dest_path, 'PNG')
        logging.info(f"Converted {source_path} to {dest_path}")
    except Exception as e:
        logging.error(f"Error converting {source_path}: {str(e)}")

def convert_jpg_to_png(source_dir, dest_dir):
    source_dir = Path(source_dir)
    dest_dir = Path(dest_dir)

    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")
    
    dest_dir.mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        for file_path in source_dir.iterdir():
            if is_image(file_path):
                png_filename = file_path.stem + ".png"
                dest_path = dest_dir / png_filename
                executor.submit(convert_image, file_path, dest_path)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        config = load_config()
        convert_jpg_to_png(config['source_directory'], config['destination_directory'])
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
