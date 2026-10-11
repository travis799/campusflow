# CampusFlow

CampusFlow is a Python command-line helpdesk ticket manager for campus technical support requests.

## Features
- Create and validate tickets with automatic IDs and rule-based priority.
- List all tickets and view one ticket.
- Assign tickets to staff.
- Manage the `open -> in_progress -> resolved` workflow.
- Display an ordered unresolved work queue.
- Report totals by status and priority.
- Save and reload tickets using JSON.
- Run automated tests with `unittest`.

## Requirements
Python 3.10 or newer. No third-party packages are required.

## Run
From the project root:

```bash
python main.py
```

Tickets are saved in `data/tickets.json`. If the file is missing, CampusFlow starts with an empty ticket list. Invalid JSON is reported rather than silently replacing the file.

## Test
```bash
python -m unittest discover -s tests -v
```

## Priority rules
Rules are checked in this order:
1. High urgency and at least 10 affected users: `critical`
2. High urgency or at least 10 affected users: `high`
3. Medium urgency or at least 3 affected users: `medium`
4. Otherwise: `low`

## Team
Fill in both fellows' names, roles, repository link and reviewed PR links before submission.

## Known limitations
This is a small local CLI prototype. It does not have user accounts or multi-computer synchronization. A resolved ticket cannot currently be reopened through the menu; add an explicit reopen action before treating the workflow as fully complete.
