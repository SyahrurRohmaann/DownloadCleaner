#!/usr/bin/env python3
import os
import shutil
import argparse
import json
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

HISTORY_FILE = ".cleaner_history.json"

def get_category(extension):
    for category, extensions in EXTENSION_MAP.items():
        if extension.lower() in extensions:
            return category
    return 'Others'

def load_history(source_path):
    history_file = source_path / HISTORY_FILE
    if history_file.exists():
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

def save_history(source_path, history):
    history_file = source_path / HISTORY_FILE
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)

def undo_move(source_dir, verbose=False):
    source_path = Path(source_dir).expanduser().resolve()
    history = load_history(source_path)

    if not history:
        print(f"No history found in {source_path}. Nothing to undo.")
        return

    print(f"Reversing {len(history)} moves...")
    undo_count = 0

    for entry in history:
        old_path = Path(entry['old_path'])
        new_path = Path(entry['new_path'])

        if new_path.exists():
            try:
                shutil.move(str(new_path), str(old_path))
                undo_count += 1
                if verbose:
                    print(f"Restored: '{new_path.name}' -> original position")
            except Exception as e:
                print(f"Error restoring '{new_path.name}': {e}")
        else:
            print(f"Skip: '{new_path.name}' not found (maybe moved/deleted manually).")

    (source_path / HISTORY_FILE).unlink()
    print(f"Undo completed. {undo_count} files restored.")

def organize_files(source_dir, dry_run=False, verbose=False):
    source_path = Path(source_dir).expanduser().resolve()
    
    if not source_path.exists() or not source_path.is_dir():
        print(f"Error: Directory '{source_path}' not found.")
        return

    print(f"Processing directory: {source_path}")
    if dry_run:
        print("--- DRY RUN MODE: No files will be moved ---")

    moved_count = 0
    history = []
    script_name = Path(sys.argv[0]).name

    for item in source_path.iterdir():
        if item.is_file() and not item.name.startswith('.') and item.name != script_name:
            category = get_category(item.suffix)
            target_dir = source_path / category
            target_file = target_dir / item.name

            if target_file.exists() and not dry_run:
                if verbose: print(f"Skipped: '{item.name}' already exists in {category}")
                continue

            if dry_run:
                if verbose: print(f"[Dry-Run] Move: '{item.name}' -> '{category}/'")
            else:
                try:
                    target_dir.mkdir(exist_ok=True)
                    history.append({
                        "old_path": str(item),
                        "new_path": str(target_file)
                    })
                    
                    shutil.move(str(item), str(target_file))
                    moved_count += 1
                    if verbose: print(f"Moved: '{item.name}' -> '{category}/'")
                except Exception as e:
                    print(f"Error moving '{item.name}': {e}")

    if not dry_run and history:
        save_history(source_path, history)

    print(f"Done. {moved_count} files moved.")

def main():
    parser = argparse.ArgumentParser(description="Organize files and undo operations.")
    parser.add_argument("--source", type=str, default=".", help="Source directory")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the process")
    parser.add_argument("--verbose", action="store_true", help="Detailed output")
    parser.add_argument("--undo", action="store_true", help="Undo the last organize operation")

    args = parser.parse_args()

    if args.undo:
        undo_move(args.source, args.verbose)
    else:
        organize_files(args.source, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()
