import unittest

from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    find_ticket,
)

class TicketTests(unittest.TestCase):

    def test_high_urgency_and_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_and_few_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_urgency_and_four_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_urgency_and_one_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_medium_urgency_is_at_least_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_zero_users_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Wi-Fi problem", "Network", "high", 0)

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "   ", "Network", "high", 2)

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Broken laptop", "Food", "low", 1)

    def test_ticket_id_increments(self):
        tickets = []

        first = create_ticket(tickets, "Problem one", "Software", "low", 1)
        second = create_ticket(tickets, "Problem two", "Hardware", "low", 1)

        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")

    def test_invalid_creation_does_not_change_tickets(self):
        tickets = []
        create_ticket(tickets, "Valid problem", "Software", "low", 1)
        original = [ticket.copy() for ticket in tickets]

        with self.assertRaises(ValueError):
            create_ticket(tickets, "", "Software", "low", 1)

        self.assertEqual(tickets, original)

    def test_find_ticket_ignores_id_case(self):
        tickets = []
        created = create_ticket(tickets, "Wi-Fi", "Network", "high", 12)

        self.assertIs(find_ticket(tickets, "t001"), created)

if __name__ == "__main__":
    unittest.main()