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

## Usage for Linux

1.  Clone the repository.
2.  Enter directory

```bash
cd DownloadCleaner
```

3. Give permission

```bash
chmod +x cleaner.py
```

5. Move to system path

```bash
sudo cp cleaner.py /usr/local/bin/cleaner
```

### Options

- `--source`: Specify the directory to clean (default: current directory).
- `--dry-run`: Simulate the cleaning process without moving files.
- `--verbose`: Show detailed output of operations.

## Example

```bash
python cleaner.py --source ~/Downloads --dry-run --verbose
```
