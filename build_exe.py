import PyInstaller.__main__
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the main script
main_script = os.path.join(script_dir, 'jpg2png.py')

# Build single executable for both GUI and CLI
PyInstaller.__main__.run([
    main_script,
    '--onefile',
    '--name=JPGtoPNGConverter',
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.filedialog',
])