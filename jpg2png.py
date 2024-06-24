import os
import json
from PIL import Image
import sys

def load_config():
    # Determine the path to the config file relative to the executable
    if getattr(sys, 'frozen', False):  # If running as a bundled executable
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)

    config_file = os.path.join(application_path, 'config.json')
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def convert_jpg_to_png(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for filename in os.listdir(source_dir):
        if filename.lower().endswith((".jpg", ".jpeg")):
            img = Image.open(os.path.join(source_dir, filename))
            png_filename = os.path.splitext(filename)[0] + ".png"
            img.save(os.path.join(dest_dir, png_filename))
            print(f"Converted {filename} to {png_filename}")

def main():
    config = load_config()
    
    source_directory = config['source_directory']
    destination_directory = config['destination_directory']

    convert_jpg_to_png(source_directory, destination_directory)

if __name__ == "__main__":
    main()
