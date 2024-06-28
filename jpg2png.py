import os
import logging
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import sys
from pathlib import Path
import threading
import argparse

class JPGtoPNGConverter:
    def __init__(self):
        self.source_dir = ""
        self.dest_dir = ""
        self.total_files = 0
        self.converted_files = 0

    def is_image(self, file_path):
        try:
            with Image.open(file_path) as img:
                return img.format in ['JPEG', 'JPG']
        except:
            return False

    def convert_jpg_to_png(self):
        source_dir = Path(self.source_dir)
        dest_dir = Path(self.dest_dir)

        if not source_dir.exists():
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")
        
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise PermissionError(f"Permission denied: Unable to create or access the destination directory '{dest_dir}'.")

        # Get list of existing PNG files in destination directory
        existing_pngs = {f.stem for f in dest_dir.glob('*.png')}

        image_files = [f for f in source_dir.iterdir() if self.is_image(f)]
        self.total_files = len(image_files)
        self.converted_files = 0

        for file_path in image_files:
            if file_path.stem not in existing_pngs:
                png_filename = file_path.stem + ".png"
                dest_path = dest_dir / png_filename
                self.convert_image(file_path, dest_path)
            else:
                self.converted_files += 1
                self.update_progress()

    def convert_image(self, source_path, dest_path):
        try:
            img = Image.open(source_path)
            img.save(dest_path, 'PNG')
            logging.info(f"Converted {source_path} to {dest_path}")
            self.converted_files += 1
            self.update_progress()
        except Exception as e:
            error_msg = f"Error converting {source_path}: {str(e)}"
            logging.error(error_msg)
            if hasattr(self, 'root'):
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))

    def update_progress(self):
        progress = int(self.converted_files / self.total_files * 100)
        if hasattr(self, 'progress_var'):
            self.progress_var.set(progress)
            self.status_label.config(text=f"Converting... {progress}% ({self.converted_files}/{self.total_files})")
        else:
            print(f"Progress: {progress}% ({self.converted_files}/{self.total_files})", end='\r')

    def run_gui(self):
        self.root = tk.Tk()
        self.root.title("JumPinG PeNGuin - JPG to PNG Converter")

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

        self.root.mainloop()

    def browse_directory(self, entry):
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

    def start_conversion(self):
        self.source_dir = self.source_entry.get()
        self.dest_dir = self.dest_entry.get()
        
        if not os.path.exists(self.source_dir):
            messagebox.showerror("Error", f"Source directory does not exist: {self.source_dir}")
            return
        
        if not os.access(self.source_dir, os.R_OK):
            messagebox.showerror("Error", f"No read permission for source directory: {self.source_dir}")
            return
        
        parent_dest = os.path.dirname(self.dest_dir)
        if not os.path.exists(parent_dest):
            messagebox.showerror("Error", f"Parent of destination directory does not exist: {parent_dest}")
            return
        
        if not os.access(parent_dest, os.W_OK):
            messagebox.showerror("Error", f"No write permission for parent of destination directory: {parent_dest}")
            return
        
        self.status_label.config(text="Converting...")
        self.progress_var.set(0)
        self.root.update()

        # Run conversion in a separate thread
        threading.Thread(target=self.run_conversion, daemon=True).start()

    def run_conversion(self):
        try:
            self.convert_jpg_to_png()
            if hasattr(self, 'root'):
                self.root.after(0, self.update_status, f"Conversion complete. Converted {self.converted_files} files.")
        except Exception as e:
            if hasattr(self, 'root'):
                self.root.after(0, lambda: messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}"))

    def update_status(self, message):
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)

    def run_cli(self, source, destination):
        self.source_dir = source
        self.dest_dir = destination

        print(f"Converting JPG images from {self.source_dir} to PNG in {self.dest_dir}")
        self.convert_jpg_to_png()
        print(f"\nConversion complete. Converted {self.converted_files} files.")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    converter = JPGtoPNGConverter()
    
    parser = argparse.ArgumentParser(description='Convert JPG images to PNG format.')
    parser.add_argument('source', nargs='?', help='Source directory containing JPG images')
    parser.add_argument('destination', nargs='?', help='Destination directory for PNG images')
    args = parser.parse_args()

    if args.source and args.destination:
        converter.run_cli(args.source, args.destination)
    else:
        converter.run_gui()

if __name__ == "__main__":
    main()