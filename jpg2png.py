import os
import json
import logging
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
import sys
import imghdr
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import threading

class JPGtoPNGConverter:
    def __init__(self):
        self.source_dir = ""
        self.dest_dir = ""
        self.total_files = 0
        self.converted_files = 0

    def load_config(self):
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))

            config_file = os.path.join(application_path, 'config.json')
            with open(config_file, 'r') as file:
                config = json.load(file)

            required_keys = ['source_directory', 'destination_directory']
            for key in required_keys:
                if key not in config:
                    raise KeyError(f"Missing required key in config: {key}")
                if not isinstance(config[key], str) or not config[key]:
                    raise ValueError(f"Invalid value for {key} in config")

            return config
        except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as e:
            logging.error(f"Error loading config: {str(e)}")
            return None

    def is_image(self, file_path):
        return imghdr.what(file_path) in ['jpeg', 'jpg']

    def convert_image(self, source_path, dest_path):
        try:
            img = Image.open(source_path)
            img.save(dest_path, 'PNG')
            logging.info(f"Converted {source_path} to {dest_path}")
            self.converted_files += 1
            self.root.after(0, self.update_progress)
        except Exception as e:
            logging.error(f"Error converting {source_path}: {str(e)}")


    def convert_jpg_to_png(self):
        source_dir = Path(self.source_dir)
        dest_dir = Path(self.dest_dir)

        if not source_dir.exists():
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")
        
        dest_dir.mkdir(parents=True, exist_ok=True)

        image_files = [f for f in source_dir.iterdir() if self.is_image(f)]
        self.total_files = len(image_files)
        self.converted_files = 0

        with ThreadPoolExecutor() as executor:
            futures = []
            for file_path in image_files:
                png_filename = file_path.stem + ".png"
                dest_path = dest_dir / png_filename
                futures.append(executor.submit(self.convert_image, file_path, dest_path))
            
            for future in futures:
                future.result()

    def run_cli(self):
        config = self.load_config()
        if config:
            self.source_dir = config['source_directory']
            self.dest_dir = config['destination_directory']
            self.convert_jpg_to_png()
        else:
            print("Failed to load configuration. Please check your config.json file.")

    def run_gui(self):
        self.root = tk.Tk()
        self.root.title("JPG to PNG Converter")

        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Source Directory:").grid(column=0, row=0, sticky=tk.W)
        ttk.Label(frame, text="Destination Directory:").grid(column=0, row=1, sticky=tk.W)

        self.source_entry = ttk.Entry(frame, width=50)
        self.source_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))
        self.dest_entry = ttk.Entry(frame, width=50)
        self.dest_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))

        ttk.Button(frame, text="Browse", command=lambda: self.browse_directory(self.source_entry)).grid(column=2, row=0)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_directory(self.dest_entry)).grid(column=2, row=1)

        ttk.Button(frame, text="Convert", command=self.start_conversion).grid(column=1, row=2)

        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(frame, length=200, mode='determinate', variable=self.progress_var)
        self.progress_bar.grid(column=1, row=3, pady=10)

        self.status_label = ttk.Label(frame, text="")
        self.status_label.grid(column=1, row=4)

        config = self.load_config()
        if config:
            self.source_entry.insert(0, config['source_directory'])
            self.dest_entry.insert(0, config['destination_directory'])

        self.root.mainloop()

    def browse_directory(self, entry):
        directory = filedialog.askdirectory()
        entry.delete(0, tk.END)
        entry.insert(0, directory)

    def start_conversion(self):
        self.source_dir = self.source_entry.get()
        self.dest_dir = self.dest_entry.get()
        self.status_label.config(text="Converting...")
        self.progress_var.set(0)
        self.root.update()

        # Run conversion in a separate thread
        threading.Thread(target=self.run_conversion, daemon=True).start()

    def run_conversion(self):
        try:
            self.convert_jpg_to_png()
            self.root.after(0, self.update_status, f"Conversion complete. Converted {self.converted_files} files.")
        except Exception as e:
            self.root.after(0, self.update_status, f"Error: {str(e)}")

    def update_status(self, message):
        self.status_label.config(text=message)
    
    def update_progress(self):
        progress = int(self.converted_files / self.total_files * 100)
        self.progress_var.set(progress)
        self.status_label.config(text=f"Converting... {progress}%")



def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    converter = JPGtoPNGConverter()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        converter.run_cli()
    else:
        converter.run_gui()

if __name__ == "__main__":
    main()