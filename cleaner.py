import os
import shutil
import argparse
from pathlib import Path

# Configuration: Mapping extensions to folder names
EXTENSION_MAP = {
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls', '.pptx', '.ppt', '.odt', '.ods', '.odp'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.tiff', '.webp'],
    'Videos': ['.mp4', '.mkv', '.mov', '.avi', '.wmv', '.flv', '.webm'],
    'Music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', '.iso'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs', '.swift', '.kt'],
    'Executables': ['.exe', '.msi', '.deb', '.sh', '.bat', '.cmd', '.app', '.dmg', '.pkg'],
    'Torrents': ['.torrent'],
}

def get_category(extension):
    """Returns the category for a given file extension."""
    for category, extensions in EXTENSION_MAP.items():
        if extension.lower() in extensions:
            return category
    return 'Others'

def organize_files(source_dir, dry_run=False, verbose=False):
    """Organizes files in the source directory into subfolders."""
    source_path = Path(source_dir).expanduser().resolve()

    if not source_path.exists():
        print(f"Error: Source directory '{source_path}' does not exist.")
        return

    if not source_path.is_dir():
        print(f"Error: '{source_path}' is not a directory.")
        return

    print(f"Processing directory: {source_path}")
    if dry_run:
        print("--- DRY RUN MODE: No files will be moved ---")

    moved_count = 0
    for item in source_path.iterdir():
        if item.is_file() and not item.name.startswith('.'): # Skip hidden files
            category = get_category(item.suffix)
            target_dir = source_path / category

            if not dry_run:
                target_dir.mkdir(exist_ok=True)

            target_file = target_dir / item.name

            # Avoid overwriting existing files
            if target_file.exists() and not dry_run: # Simple collision handling: skip
                 if verbose:
                    print(f"Skipped: '{item.name}' (File already exists in {category})")
                 continue
            
            # TODO: Improve collision handling (e.g. rename)

            if dry_run:
                 if verbose:
                    print(f"[Dry-Run] Would move: '{item.name}' -> '{category}/{item.name}'")
            else:
                try:
                    shutil.move(str(item), str(target_file))
                    if verbose:
                        print(f"Moved: '{item.name}' -> '{category}/{item.name}'")
                    moved_count += 1
                except Exception as e:
                    print(f"Error moving '{item.name}': {e}")

    print(f"Done. {moved_count} files moved.")


def main():
    parser = argparse.ArgumentParser(description="Organize files in a directory based on their extensions.")
    parser.add_argument("--source", type=str, default=".", help="Source directory to clean (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the cleaning process without moving files")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output of operations")

    args = parser.parse_args()

    organize_files(args.source, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()
