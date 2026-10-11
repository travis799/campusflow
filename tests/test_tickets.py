import unittest
from campusflow.tickets import calculate_priority, create_ticket


class TicketTests(unittest.TestCase):
    def test_high_urgency_and_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_three_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_one_low_urgency_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_zero_users_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Wi-Fi down", "Network", "high", 0)

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "   ", "Network", "high", 2)

    def test_category_is_normalized(self):
        tickets = []
        ticket = create_ticket(tickets, "Laptop broken", "hardware", "medium", 1)
        self.assertEqual(ticket["category"], "Hardware")

    def test_ids_are_unique(self):
        tickets = []
        first = create_ticket(tickets, "First", "Other", "low", 1)
        second = create_ticket(tickets, "Second", "Other", "low", 1)
        self.assertEqual((first["id"], second["id"]), ("T001", "T002"))


if __name__ == "__main__":
    unittest.main()
