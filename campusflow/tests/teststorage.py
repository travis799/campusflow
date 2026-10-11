import json
import tempfile
import unittest
from pathlib import Path

from campusflow.tickets import create_ticket
from campusflow.storage import load_tickets, save_tickets

class StorageTests(unittest.TestCase):

    def test_save_and_reload_preserves_tickets(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            tickets = []

            create_ticket(tickets, "Wi-Fi down", "Network", "high", 12)
            save_tickets(tickets, path)

            loaded = load_tickets(path)

            self.assertEqual(loaded, tickets)

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.json"

            self.assertEqual(load_tickets(path), [])

    def test_corrupted_json_raises_clear_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            path.write_text("{bad json", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "invalid JSON"):
                load_tickets(path)

    def test_duplicate_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            record = {
                "id": "T001",
                "title": "Wi-Fi",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            }

            path.write_text(
                json.dumps([record, record]),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
                load_tickets(path)

    def test_id_remains_unique_after_reload(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            tickets = []

            create_ticket(tickets, "First", "Software", "low", 1)
            save_tickets(tickets, path)

            loaded = load_tickets(path)
            second = create_ticket(loaded, "Second", "Hardware", "low", 1)

            self.assertEqual(second["id"], "T002")

if __name__ == "__main__":
    unittest.main()