"""Ticket summary reports."""


def build_report(tickets):
    statuses = {"open": 0, "in_progress": 0, "resolved": 0}
    priorities = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for ticket in tickets:
        statuses[ticket["status"]] += 1
        priorities[ticket["priority"]] += 1

    return {
        "total": len(tickets),
        "by_status": statuses,
        "by_priority": priorities,
    }


def show_report(tickets):
    report = build_report(tickets)
    print("Total tickets:", report["total"])
    print("By status:", report["by_status"])
    print("By priority:", report["by_priority"])
