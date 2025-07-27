import unittest
import json
import os
from pathlib import Path
from tools import port_scanner

class TestPortScanner(unittest.TestCase):
    def setUp(self):
        self.output_file = Path("reports/scan_results.json")
        if self.output_file.exists():
            self.output_file.unlink()  # Clean up old results

    def tearDown(self):
        if self.output_file.exists():
            self.output_file.unlink()

    def test_scan_ports_returns_valid_result(self):
        ports_to_check = [22, 80, 443]
        result = port_scanner.scan_ports("127.0.0.1", ports_to_check)

        self.assertIsInstance(result, dict)
        self.assertEqual(set(result.keys()), set(map(str, ports_to_check)))
        for status in result.values():
            self.assertIn(status, ["open", "closed"])

    def test_main_creates_output_file(self):
        port_scanner.main()
        self.assertTrue(self.output_file.exists())

        with open(self.output_file, "r") as f:
            data = json.load(f)
            self.assertIsInstance(data, dict)
            for port, status in data.items():
                self.assertIn(status, ["open", "closed"])

if __name__ == '__main__':
    unittest.main()
