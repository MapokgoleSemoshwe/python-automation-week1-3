import os
import shutil
import argparse
import logging
from datetime import datetime
 
# Map file extensions to the folder they should land in.
# Extend this dictionary as you need more categories for your capstone.
CATEGORY_MAP = {
    ".txt": "Documents", ".pdf": "Documents", ".docx": "Documents", ".csv": "Documents",
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    ".py": "Scripts", ".sh": "Scripts", ".js": "Scripts",
    ".zip": "Archives", ".rar": "Archives", ".tar": "Archives",
    ".mp3": "Audio", ".wav": "Audio",
    ".mp4": "Video", ".mov": "Video",
}
 
 
def setup_logger(log_path: str) -> logging.Logger:
    """Create a logger that writes to both the console and a log file."""
    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()  # avoid duplicate handlers if re-run in the same session
 
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
 
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
 
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
 
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
 
 
def organize_folder(source: str, dry_run: bool = False) -> None:
    if not os.path.isdir(source):
        raise NotADirectoryError(f"'{source}' is not a valid folder.")
 
    log_path = os.path.join(source, "organizer_log.txt")
    logger = setup_logger(log_path)
    logger.info(f"Starting organisation of '{source}' (dry_run={dry_run})")
 
    seen_filenames = set()
    moved, skipped, duplicates, unrecognised = 0, 0, 0, 0
 
    for entry in os.listdir(source):
        full_path = os.path.join(source, entry)
 
        # Skip folders and the log file itself
        if os.path.isdir(full_path) or entry == "organizer_log.txt":
            continue
 
        # Detect duplicate filenames
        if entry in seen_filenames:
            logger.warning(f"Duplicate filename detected: {entry}")
            duplicates += 1
        seen_filenames.add(entry)
 
        _, ext = os.path.splitext(entry)
        ext = ext.lower()
 
        if not ext:
            logger.warning(f"File with no extension (unrecognised): {entry}")
            unrecognised += 1
            category = "Unrecognised"
        else:
            category = CATEGORY_MAP.get(ext, "Other")
 
        dest_folder = os.path.join(source, category)
        dest_path = os.path.join(dest_folder, entry)
 
        if dry_run:
            logger.info(f"[DRY RUN] Would move '{entry}' -> '{category}/'")
            continue
 
        os.makedirs(dest_folder, exist_ok=True)
 
        try:
            shutil.move(full_path, dest_path)
            logger.info(f"Moved '{entry}' -> '{category}/'")
            moved += 1
        except Exception as e:
            logger.error(f"Failed to move '{entry}': {e}")
            skipped += 1
 
    logger.info(
        f"Done. Moved={moved}, Skipped(errors)={skipped}, "
        f"Duplicates flagged={duplicates}, Unrecognised={unrecognised}"
    )
 
 
def main():
    parser = argparse.ArgumentParser(description="Organise files in a folder by type.")
    parser.add_argument("source", help="Path to the folder you want to organise")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without moving files")
    args = parser.parse_args()
 
    try:
        organize_folder(args.source, dry_run=args.dry_run)
    except Exception as e:
        print(f"Error: {e}")
 
 
if __name__ == "__main__":
    main()