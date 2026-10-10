from campusflow.tickets import find_ticket

VALID_STATUSES = {"open", "in_progress", "resolved"}

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

def assign_ticket(tickets, ticket_id, staff_name):
    """Assign an unresolved ticket to a staff member."""
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError("Reopen the resolved ticket before modifying it.")

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff member name cannot be blank.")

    ticket["assigned_to"] = staff_name.strip()
    return ticket

def change_status(tickets, ticket_id, new_status):
    """Move a ticket through its permitted workflow."""
    ticket = find_ticket(tickets, ticket_id)

    if not isinstance(new_status, str):
        raise ValueError("Status must be open, in_progress, or resolved.")

    new_status = new_status.strip().lower()

    if new_status not in VALID_STATUSES:
        raise ValueError("Invalid status.")

    current_status = ticket["status"]

    if current_status == "resolved":
        raise ValueError("Reopen the ticket explicitly before modifying it.")

    if current_status == "open" and new_status == "in_progress":
        if not ticket["assigned_to"]:
            raise ValueError("Assign the ticket before starting work.")

    allowed_transitions = {
        "open": {"in_progress"},
        "in_progress": {"resolved"},
    }

    if new_status not in allowed_transitions.get(current_status, set()):
        raise ValueError(
            f"Cannot change status from {current_status} to {new_status}."
        )

    ticket["status"] = new_status
    return ticket

def reopen_ticket(tickets, ticket_id):
    """Explicitly reopen a resolved ticket."""
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")

    ticket["status"] = "open"
    return ticket

def get_work_queue(tickets):
    """Return unresolved tickets in priority and numeric-ID order."""
    unresolved = [
        ticket for ticket in tickets
        if ticket["status"] != "resolved"
    ]

    return sorted(
        unresolved,
        key=lambda ticket: (
            PRIORITY_ORDER[ticket["priority"]],
            int(ticket["id"][1:]),
        ),
    )