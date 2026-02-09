import shutil
import argparse
import sys
from pathlib import Path

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

def generate_unique_path(target_path):
    """
    Jika file sudah ada, tambahkan angka counter di belakang nama file.
    Contoh: file.txt -> file_1.txt -> file_2.txt
    """
    if not target_path.exists():
        return target_path

    counter = 1
    stem = target_path.stem  
    suffix = target_path.suffix 
    
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = target_path.with_name(new_name)
        if not new_path.exists():
            return new_path
        counter += 1

def organize_files(source_dir, dry_run=False, verbose=False):
    source_path = Path(source_dir).expanduser().resolve()

    if not source_path.exists():
        print(f" Error: Direktori '{source_path}' tidak ditemukan.")
        return
    if not source_path.is_dir():
        print(f" Error: '{source_path}' bukan direktori.")
        return

    print(f" Memproses direktori: {source_path}")
    if dry_run:
        print("---  DRY RUN MODE: Tidak ada file yang akan dipindahkan ---\n")

    moved_count = 0
    script_name = Path(sys.argv[0]).name 

    for item in source_path.iterdir():
        if not item.is_file() or item.name.startswith('.'):
            continue
        if item.name == script_name:
            continue

        category = get_category(item.suffix)
        target_dir = source_path / category
        
        target_file = target_dir / item.name

        final_target_path = generate_unique_path(target_file)
        
        
        is_renamed = final_target_path.name != item.name
        rename_msg = f" (Renamed to {final_target_path.name})" if is_renamed else ""

        if dry_run:
            if verbose:
                print(f"[Dry-Run] Move: '{item.name}' -> '{category}/{final_target_path.name}'")
        else:
            
            try:
                target_dir.mkdir(exist_ok=True)
            
                shutil.move(str(item), str(final_target_path))
                
                moved_count += 1
                if verbose:
                    print(f"Moved: '{item.name}' -> '{category}/'{rename_msg}")
                    
            except Exception as e:
                print(f"Gagal memindahkan '{item.name}': {e}")

    print(f"\n Selesai. {moved_count} file berhasil dipindahkan.")

def main():
    parser = argparse.ArgumentParser(description="Organize files in a directory based on their extensions.")
    parser.add_argument("source", nargs="?", default=".", help="Source directory to clean (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the cleaning process without moving files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output of operations")

    args = parser.parse_args()

    organize_files(args.source, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()
