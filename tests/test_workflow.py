import unittest
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status, work_queue


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Wi-Fi down", "Network", "high", 12)
        create_ticket(self.tickets, "Mouse broken", "Hardware", "low", 1)

    def test_unassigned_ticket_cannot_start(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")

    def test_assigned_ticket_can_progress_and_resolve(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        self.assertEqual(self.tickets[0]["status"], "resolved")

    def test_queue_orders_priority(self):
        queue = work_queue(self.tickets)
        self.assertEqual([ticket["id"] for ticket in queue], ["T001", "T002"])

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(KeyError):
            assign_ticket(self.tickets, "T999", "Ada")


if __name__ == "__main__":
    unittest.main()
