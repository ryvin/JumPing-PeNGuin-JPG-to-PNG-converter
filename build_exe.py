import PyInstaller.__main__
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the main script
main_script = os.path.join(script_dir, 'jpg2png.py')

# Define the path to the config file
config_file = os.path.join(script_dir, 'config.json')

PyInstaller.__main__.run([
    main_script,
    '--onefile',
    '--windowed',
    '--name=JPGtoPNGConverter',
    f'--add-data={config_file};.',
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.filedialog',
    '--debug=all',
    '--collect-all=PIL',
])