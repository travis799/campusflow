from campusflow.tickets import PRIORITIES

STATUSES = ["open", "in_progress", "resolved"]


def generate_report(tickets):
    """Generate ticket totals grouped by status and priority."""

    report = {
        "total": len(tickets),
        "by_status": {status: 0 for status in STATUSES},
        "by_priority": {priority: 0 for priority in PRIORITIES},
    }

    for ticket in tickets:
        report["by_status"][ticket["status"]] += 1
        report["by_priority"][ticket["priority"]] += 1

    return report