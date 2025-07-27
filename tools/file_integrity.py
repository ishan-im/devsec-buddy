# tools/file_integrity.py

import hashlib
import json
from datetime import datetime
from pathlib import Path
import yaml

CONFIG_PATH = Path("configs/file_integrity.yaml")
REPORT_PATH = Path("reports/integrity_log.txt")
HASH_STORE = Path("reports/file_hashes.json")

LOG_FILE = "file_change.log"  # ✅ Define it at the module level

def compute_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def log_change(message, old_hash, new_hash):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
        f.write(f"    Old hash: {old_hash}\n")
        f.write(f"    New hash: {new_hash}\n")



def calculate_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None


def load_previous_hashes() -> dict:
    if HASH_STORE.exists():
        with open(HASH_STORE, "r") as f:
            return json.load(f)
    return {}


def save_hashes(hashes: dict):
    with open(HASH_STORE, "w") as f:
        json.dump(hashes, f, indent=2)





def run_integrity_check():
    if not CONFIG_PATH.exists():
        print("Configuration file not found.")
        return

    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    files_to_check = config.get("files", [])
    prev_hashes = load_previous_hashes()
    current_hashes = {}

    for file in files_to_check:
        path = Path(file)
        new_hash = calculate_sha256(path)
        if new_hash:
            old_hash = prev_hashes.get(file)
            if old_hash and old_hash != new_hash:
                log_change(file, old_hash, new_hash)
            current_hashes[file] = new_hash

    save_hashes(current_hashes)
