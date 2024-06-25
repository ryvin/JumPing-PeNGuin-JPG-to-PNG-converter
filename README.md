# JPG to PNG Converter

This Python script converts JPG images to PNG format using multithreading for improved performance.

## Features

- Converts JPG/JPEG images to PNG format
- Uses multithreading for faster processing
- Implements logging for better debugging and monitoring
- Includes error handling and input validation
- Provides unit tests for key functions

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/jpg-to-png-converter.git
   cd jpg-to-png-converter
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Update the `config.json` file with the correct paths:
   ```json
   {
     "source_directory": "/path/to/your/jpg/files",
     "destination_directory": "/path/to/save/png/files"
   }
   ```

2. Run the script:
   ```
   python jpg2png.py
   ```

## Configuration

The script uses a `config.json` file to specify the source and destination directories. Ensure that both paths are valid and accessible.

## How it works

1. The script reads the `config.json` file to determine the source and destination directories.
2. It iterates over all files in the source directory, checking if they are valid JPG/JPEG images.
3. For each valid image, the script converts it to PNG format and saves it in the destination directory.
4. The conversion process uses multithreading to improve performance when dealing with multiple images.
5. Logging is implemented to track the conversion process and any errors that may occur.

## Testing

To run the unit tests:

```
python -m unittest test_jpg2png.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

## Contact

Raul Pineda - raul@pinedamail.com

Project Link: [https://gitlab.leadingbit.com/raul/jpg2png](https://gitlab.leadingbit.com/raul/jpg2png)