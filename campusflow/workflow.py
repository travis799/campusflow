"""Ticket assignment, status workflow, and ordered work queue."""

from campusflow.tickets import get_ticket

ALLOWED_STATUSES = {"open", "in_progress", "resolved"}


def assign_ticket(tickets, ticket_id, staff_name):
    ticket = get_ticket(tickets, ticket_id)
    staff_name = staff_name.strip()
    if not staff_name:
        raise ValueError("Staff member name cannot be blank.")
    if ticket["status"] == "resolved":
        raise ValueError("Reopen a resolved ticket before modifying it.")
    ticket["assigned_to"] = staff_name
    return ticket


def change_status(tickets, ticket_id, new_status):
    ticket = get_ticket(tickets, ticket_id)
    new_status = new_status.strip().lower()

    if new_status not in ALLOWED_STATUSES:
        raise ValueError("Status must be open, in_progress, or resolved.")
    if ticket["status"] == "resolved":
        raise ValueError("A resolved ticket must be reopened to open first.")
    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError("Assign the ticket before moving it to in_progress.")
    if ticket["status"] == "open" and new_status == "resolved":
        raise ValueError("Move an open ticket to in_progress before resolving it.")

    ticket["status"] = new_status
    return ticket


def work_queue(tickets):
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    queue = [ticket for ticket in tickets
             if ticket["status"] in {"open", "in_progress"}]
    return sorted(
        queue,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            int(ticket["id"][1:])
        )
    )
