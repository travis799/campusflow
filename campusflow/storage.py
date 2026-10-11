"""JSON persistence for tickets."""

import json
import os


def load_tickets(filename):
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"{filename} contains invalid JSON.") from error

    if not isinstance(data, list):
        raise ValueError(f"{filename} must contain a JSON list of tickets.")
    return data


def save_tickets(filename, tickets):
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)

    # Write a temporary file first, then replace the old file.
    temporary = filename + ".tmp"
    with open(temporary, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=2)
        file.write("\n")
    os.replace(temporary, filename)
