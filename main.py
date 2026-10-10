from campusflow.tickets import create_ticket, find_ticket
from campusflow.workflow import (
    assign_ticket,
    change_status,
    reopen_ticket,
    get_work_queue,
)
from campusflow.storage import load_tickets, save_tickets
from campusflow.reports import generate_report

def show_ticket(ticket):
    """Display all fields of one ticket."""
    for key, value in ticket.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("-" * 40)

def read_affected_users():
    """Read a positive whole number from the user."""
    raw_value = input("Number of affected users: ").strip()

    try:
        value = int(raw_value)
    except ValueError:
        raise ValueError("Affected users must be a positive whole number.")

    if value <= 0:
        raise ValueError("Affected users must be greater than zero.")

    return value

def main():
    try:
        tickets = load_tickets()
    except ValueError as error:
        print(f"Storage error: {error}")
        print("Fix the data file before restarting CampusFlow.")
        return

    print("Welcome to CampusFlow Helpdesk!")

    while True:
        print("""
========== CAMPUSFLOW ==========
1. Create ticket
2. List all tickets
3. View one ticket
4. Assign ticket
5. Change ticket status
6. Reopen resolved ticket
7. View work queue
8. View reports
9. Save tickets
0. Exit
================================
""")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                title = input("Ticket title: ")
                category = input(
                    "Category (Network/Hardware/Software/Other): "
                )
                urgency = input("Urgency (low/medium/high): ")
                affected_users = read_affected_users()

                ticket = create_ticket(
                    tickets, title, category, urgency, affected_users
                )

                save_tickets(tickets)
                print("Ticket created successfully!")
                show_ticket(ticket)

            elif choice == "2":
                if not tickets:
                    print("No tickets found.")
                else:
                    for ticket in tickets:
                        show_ticket(ticket)

            elif choice == "3":
                ticket_id = input("Enter ticket ID: ")
                show_ticket(find_ticket(tickets, ticket_id))

            elif choice == "4":
                ticket_id = input("Enter ticket ID: ")
                staff_name = input("Staff member name: ")

                ticket = assign_ticket(tickets, ticket_id, staff_name)
                save_tickets(tickets)
                print("Ticket assigned successfully.")
                show_ticket(ticket)

            elif choice == "5":
                ticket_id = input("Enter ticket ID: ")
                status = input(
                    "New status (in_progress/resolved): "
                )

                ticket = change_status(tickets, ticket_id, status)
                save_tickets(tickets)
                print("Ticket status updated.")
                show_ticket(ticket)

            elif choice == "6":
                ticket_id = input("Enter resolved ticket ID: ")
                ticket = reopen_ticket(tickets, ticket_id)
                save_tickets(tickets)
                print("Ticket reopened.")
                show_ticket(ticket)

            elif choice == "7":
                queue = get_work_queue(tickets)

                if not queue:
                    print("The work queue is empty.")
                else:
                    for ticket in queue:
                        print(
                            f"{ticket['id']} | "
                            f"{ticket['priority']} | "
                            f"{ticket['status']} | "
                            f"{ticket['title']}"
                        )

            elif choice == "8":
                report = generate_report(tickets)

                print(f"Total tickets: {report['total']}")
                print("By status:")

                for status, count in report["by_status"].items():
                    print(f"  {status}: {count}")

                print("By priority:")

                for priority, count in report["by_priority"].items():
                    print(f"  {priority}: {count}")

            elif choice == "9":
                save_tickets(tickets)
                print("Tickets saved.")

            elif choice == "0":
                save_tickets(tickets)
                print("Tickets saved. Goodbye!")
                break

            else:
                print("Invalid menu choice. Please choose 0-9.")

        except ValueError as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()