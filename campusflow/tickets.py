"""Ticket creation, validation, priority calculation, and viewing."""

CATEGORIES = {"network": "Network", "hardware": "Hardware",
              "software": "Software", "other": "Other"}
URGENCIES = {"low", "medium", "high"}


def calculate_priority(urgency, affected_users):
    """Apply the assignment's priority rules in the required order."""
    urgency = urgency.lower()

    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def create_ticket(tickets, title, category, urgency, affected_users):
    title = title.strip()
    if not title:
        raise ValueError("Title cannot be blank.")

    category_key = category.strip().lower()
    if category_key not in CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    urgency = urgency.strip().lower()
    if urgency not in URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")

    if isinstance(affected_users, bool) or not isinstance(affected_users, int):
        raise ValueError("Affected users must be a whole number.")
    if affected_users <= 0:
        raise ValueError("Affected users must be greater than zero.")

    # Find the largest existing number so IDs stay unique after reload.
    numbers = [int(ticket["id"][1:]) for ticket in tickets
               if ticket.get("id", "").startswith("T")
               and ticket["id"][1:].isdigit()]
    next_number = max(numbers, default=0) + 1

    ticket = {
        "id": f"T{next_number:03d}",
        "title": title,
        "category": CATEGORIES[category_key],
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket


def list_tickets(tickets):
    if not tickets:
        print("No tickets found.")
        return
    for ticket in tickets:
        print(ticket)


def get_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise KeyError(f"Unknown ticket ID: {ticket_id}")
