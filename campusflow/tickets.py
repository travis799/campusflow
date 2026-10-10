PRIORITIES = ["critical", "high", "medium", "low"]
CATEGORIES = ["Network", "Hardware", "Software", "Other"]
URGENCY_LEVELS = ["low", "medium", "high"]

def calculate_priority(urgency, affected_users):
    """Calculate priority using the assignment's exact rule order."""
    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"

def validate_ticket_input(title, category, urgency, affected_users):
    """Validate and normalize ticket fields."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title cannot be blank.")

    if not isinstance(category, str):
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    category_lookup = {item.lower(): item for item in CATEGORIES}
    category = category_lookup.get(category.strip().lower())

    if category is None:
        raise ValueError("Invalid category. Choose Network, Hardware, Software, or Other.")

    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")

    urgency = urgency.strip().lower()

    if urgency not in URGENCY_LEVELS:
        raise ValueError("Invalid urgency. Choose low, medium, or high.")

    # bool must be rejected because True and False are also integers in Python.
    if type(affected_users) is not int or affected_users <= 0:
        raise ValueError("Affected users must be a positive whole number.")

    return title.strip(), category, urgency, affected_users

def next_ticket_id(tickets):
    """Generate the next ID using the largest existing numeric ID."""
    highest_number = 0

    for ticket in tickets:
        ticket_id = ticket.get("id", "")

        if isinstance(ticket_id, str) and ticket_id.startswith("T"):
            number_part = ticket_id[1:]

            if number_part.isdigit():
                highest_number = max(highest_number, int(number_part))

    return f"T{highest_number + 1:03d}"

def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate details, create a ticket and add it to the collection."""

    title, category, urgency, affected_users = validate_ticket_input(
        title, category, urgency, affected_users
    )

    ticket = {
        "id": next_ticket_id(tickets),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }

    tickets.append(ticket)
    return ticket

def find_ticket(tickets, ticket_id):
    """Find a ticket by ID or raise a useful error."""
    if not isinstance(ticket_id, str):
        raise ValueError("Ticket ID must be text.")

    for ticket in tickets:
        if ticket["id"].lower() == ticket_id.strip().lower():
            return ticket

    raise ValueError(f"Ticket {ticket_id!r} was not found.")