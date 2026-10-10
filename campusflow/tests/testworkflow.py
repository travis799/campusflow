import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket,
    change_status,
    reopen_ticket,
    get_work_queue,
)

class WorkflowTests(unittest.TestCase):

    def setUp(self):
        self.tickets = []

    def make_ticket(self, title, urgency, users):
        return create_ticket(
            self.tickets, title, "Network", urgency, users
        )

    def test_unassigned_ticket_cannot_start(self):
        ticket = self.make_ticket("Wi-Fi", "high", 12)

        with self.assertRaises(ValueError):
            change_status(self.tickets, ticket["id"], "in_progress")

        self.assertEqual(ticket["status"], "open")

    def test_assigned_ticket_can_be_resolved(self):
        ticket = self.make_ticket("Wi-Fi", "high", 12)

        assign_ticket(self.tickets, ticket["id"], "Ada")
        change_status(self.tickets, ticket["id"], "in_progress")
        change_status(self.tickets, ticket["id"], "resolved")

        self.assertEqual(ticket["status"], "resolved")

    def test_blank_staff_name_is_rejected(self):
        ticket = self.make_ticket("Laptop", "low", 1)

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, ticket["id"], " ")

        self.assertIsNone(ticket["assigned_to"])

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Ada")

    def test_resolved_ticket_must_be_reopened(self):
        ticket = self.make_ticket("Laptop", "low", 1)

        assign_ticket(self.tickets, ticket["id"], "Ada")
        change_status(self.tickets, ticket["id"], "in_progress")
        change_status(self.tickets, ticket["id"], "resolved")

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, ticket["id"], "Sam")

        reopen_ticket(self.tickets, ticket["id"])
        assign_ticket(self.tickets, ticket["id"], "Sam")

        self.assertEqual(ticket["status"], "open")
        self.assertEqual(ticket["assigned_to"], "Sam")

    def test_queue_uses_priority_then_numeric_id(self):
        low = self.make_ticket("Low", "low", 1)
        high_1 = self.make_ticket("High one", "high", 2)
        high_2 = self.make_ticket("High two", "high", 3)
        critical = self.make_ticket("Critical", "high", 12)

        queue = get_work_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            [critical["id"], high_1["id"], high_2["id"], low["id"]],
        )

    def test_resolved_tickets_are_not_in_queue(self):
        ticket = self.make_ticket("Laptop", "low", 1)

        assign_ticket(self.tickets, ticket["id"], "Ada")
        change_status(self.tickets, ticket["id"], "in_progress")
        change_status(self.tickets, ticket["id"], "resolved")

        self.assertEqual(get_work_queue(self.tickets), [])

if __name__ == "__main__":
    unittest.main()