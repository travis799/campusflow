# CampusFlow design decisions

## Shared data structure
Tickets are stored as a list of dictionaries. Each dictionary contains `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, and `assigned_to`.

## Module ownership
- `campusflow/tickets.py`: validation, priority, ticket IDs, listing and lookup.
- `campusflow/workflow.py`: assignment, status transitions and queue sorting.
- `campusflow/reports.py`: totals and status/priority counts.
- `campusflow/storage.py`: JSON loading and saving.
- `main.py`: command-line menu and user interaction.

## Error handling
Business functions raise `ValueError` for invalid values and `KeyError` for unknown ticket IDs. The CLI catches these and prints a readable message.

## Testing
Business logic functions accept normal arguments instead of calling `input()`, so tests can call them directly without interactive prompts.

## Team ownership (fill in together)
- Fellow A:
- Fellow B:
- Branch names:
- GitHub repository URL:
