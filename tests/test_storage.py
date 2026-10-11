import json
import os
import tempfile
import unittest
from campusflow.storage import load_tickets, save_tickets


class StorageTests(unittest.TestCase):
    def test_save_and_reload(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "tickets.json")
            original = [{"id": "T001", "title": "Wi-Fi down"}]
            save_tickets(filename, original)
            self.assertEqual(load_tickets(filename), original)

    def test_missing_file_starts_empty(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(load_tickets(os.path.join(folder, "missing.json")), [])

    def test_malformed_json_raises_clear_error(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "tickets.json")
            with open(filename, "w", encoding="utf-8") as file:
                file.write("{broken")
            with self.assertRaisesRegex(ValueError, "invalid JSON"):
                load_tickets(filename)


if __name__ == "__main__":
    unittest.main()
