# main.py
from tools import file_integrity

paths = ["/etc/passwd", "/etc/hosts"]  # configurable later
hash_db = {}  # In-memory for now

modified_files = file_integrity.check_files(paths, hash_db)
if modified_files:
    print("[!] Changes detected:", modified_files)
else:
    print("[✓] No changes")
