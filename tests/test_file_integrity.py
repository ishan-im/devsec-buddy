import unittest
import os
from pathlib import Path
from tools import file_integrity

class TestFileIntegrity(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_sample.txt"
        with open(self.test_file, "w") as f:
            f.write("Initial content")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        log_path = Path("reports/integrity_log.txt")
        if log_path.exists():
            log_path.unlink()

    def test_compute_hash_changes_on_modification(self):
        hash1 = file_integrity.compute_hash(self.test_file)
        self.assertIsInstance(hash1, str)

        # Modify the file
        with open(self.test_file, "w") as f:
            f.write("Modified content")

        hash2 = file_integrity.compute_hash(self.test_file)
        self.assertNotEqual(hash1, hash2)

    def test_log_change_creates_log_file(self):
        message = "Sample change detected."
        file_integrity.log_change(message)
        log_path = Path("reports/integrity_log.txt")
        self.assertTrue(log_path.exists())

        with open(log_path) as f:
            content = f.read()
            self.assertIn(message, content)

if __name__ == '__main__':
    unittest.main()
