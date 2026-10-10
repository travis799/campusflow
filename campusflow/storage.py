import json
from pathlib import Path


DEFAULT_PATH = Path("data/tickets.json")


def save_tickets(tickets, path=DEFAULT_PATH):
    """Save tickets to a JSON file."""
    path = Path(path)

    # Create the parent directory if it doesn't exist.
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(path=DEFAULT_PATH):
    """Load tickets from a JSON file."""
    path = Path(path)

    # A missing file means there are no saved tickets yet.
    if not path.exists():
        return []

    # Read the JSON data.
    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)

    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError(
            f"Cannot load ticket data from {path}: invalid JSON."
        ) from error

    # The saved data must be a list.
    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a JSON list.")

    required_fields = {
        "id",
        "title",
        "category",
        "urgency",
        "affected_users",
        "priority",
        "status",
        "assigned_to",
    }

    seen_ids = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Ticket data contains an invalid ticket record.")

        if not required_fields.issubset(ticket):
            raise ValueError("Ticket data contains an invalid ticket record.")

        ticket_id = ticket["id"]

        if not isinstance(ticket_id, str) or not ticket_id.strip():
            raise ValueError("Ticket data contains an invalid ticket ID.")

        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID found: {ticket_id}")

        seen_ids.add(ticket_id)

    return tickets