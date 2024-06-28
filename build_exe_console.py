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
    '--name=JPGtoPNGConverter_Console',
    f'--add-data={config_file};.',
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.filedialog',
    '--hidden-import=PIL',
    '--hidden-import=PIL._imagingtk',
    '--hidden-import=PIL._tkinter_finder',
    '--clean',
    '--noconfirm',
])