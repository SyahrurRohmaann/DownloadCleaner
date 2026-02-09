# Desktop/Download Cleaner

A simple CLI tool to organize your Downloads folder by moving files into specific subfolders based on their extensions.

## Features

- Organizes files into categories:
    - **Documents**: .pdf, .docx, .txt, .xlsx, .pptx
    - **Images**: .jpg, .jpeg, .png, .gif, .svg
    - **Videos**: .mp4, .mkv, .mov, .avi
    - **Music**: .mp3, .wav, .flac
    - **Archives**: .zip, .rar, .tar, .7z
    - **Code**: .py, .js, .html, .css, .java, .cpp
    - **Executables**: .exe, .msi, .deb, .sh
- Supports custom source directory.
- Dry-run mode to preview changes without moving files.
- Verbose mode for detailed output.

## Usage

1.  Clone the repository.
2.  Run the script:

```bash
python cleaner.py --source /path/to/directory
```

### Options

- `--source`: Specify the directory to clean (default: current directory).
- `--dry-run`: Simulate the cleaning process without moving files.
- `--verbose`: Show detailed output of operations.

## Example

```bash
python cleaner.py --source ~/Downloads --dry-run --verbose
```
