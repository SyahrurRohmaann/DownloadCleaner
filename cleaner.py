import shutil
import argparse
import sys
import json
from pathlib import Path

HISTORY_FILE = ".cleaner_history.json"

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

def save_history(history_data, source_dir):
    history_path = Path(source_dir) / HISTORY_FILE
    with open(history_path, 'w') as f:
        json.dump(history_data, f, indent=4)

def load_history(source_dir):
    history_path = Path(source_dir) / HISTORY_FILE
    if history_path.exists():
        with open(history_path, 'r') as f:
            return json.load(f)
    return []

def get_category(extension):
    for category, extensions in EXTENSION_MAP.items():
        if extension.lower() in extensions:
            return category
    return 'Others'

def generate_unique_path(target_path):
    if not target_path.exists():
        return target_path
    counter = 1
    stem, suffix = target_path.stem, target_path.suffix
    while True:
        new_path = target_path.with_name(f"{stem}_{counter}{suffix}")
        if not new_path.exists():
            return new_path
        counter += 1

def organize_files(source_dir, dry_run=False, verbose=False):
    source_path = Path(source_dir).expanduser().resolve()
    if not source_path.exists() or not source_path.is_dir():
        print(f"❌ Error: Folder {source_path} tidak valid.")
        return

    print(f"📂 Memproses direktori: {source_path}")
    history_data = []
    moved_count = 0
    script_name = Path(sys.argv[0]).name

    for item in source_path.iterdir():
        if not item.is_file() or item.name.startswith('.') or item.name == script_name:
            continue

        category = get_category(item.suffix)
        target_dir = source_path / category
        final_target_path = generate_unique_path(target_dir / item.name)

        if dry_run:
            if verbose: print(f"[Dry-Run] Would move: {item.name} -> {category}/")
        else:
            try:
                target_dir.mkdir(exist_ok=True)
                history_data.append({
                    "old": str(item.absolute()),
                    "new": str(final_target_path.absolute())
                })
                shutil.move(str(item), str(final_target_path))
                moved_count += 1
                if verbose: print(f"✅ Moved: {item.name} -> {category}/")
            except Exception as e:
                print(f"❌ Gagal memindahkan {item.name}: {e}")

    if not dry_run and history_data:
        save_history(history_data, source_path)
    
    print(f"\n✨ Selesai. {moved_count} file berhasil dipindahkan.")

def undo_move(source_dir):
    source_path = Path(source_dir).expanduser().resolve()
    history = load_history(source_path)

    if not history:
        print("ℹ️ Tidak ada histori pemindahan yang ditemukan di folder ini.")
        return

    print(f"⏪ Membatalkan {len(history)} pemindahan terakhir...")
    undo_count = 0
    for entry in history:
        current_loc, original_loc = Path(entry['new']), Path(entry['old'])
        if current_loc.exists():
            try:
                shutil.move(str(current_loc), str(original_loc))
                undo_count += 1
            except Exception as e:
                print(f"❌ Gagal mengembalikan {current_loc.name}: {e}")

    (source_path / HISTORY_FILE).unlink() 
    print(f"✅ Berhasil mengembalikan {undo_count} file.")

def main():
    parser = argparse.ArgumentParser(description="Organize files in a directory.")
    parser.add_argument("source", nargs="?", default=".", help="Source directory")
    parser.add_argument("--dry-run", action="store_true", help="Simulate only")
    parser.add_argument("--undo", action="store_true", help="Undo last operation")
    parser.add_argument("-v", "--verbose", action="store_true", help="Detail logs")

    args = parser.parse_args()

    if args.undo:
        undo_move(args.source)
    else:
        organize_files(args.source, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()
