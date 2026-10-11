from campusflow.tickets import create_ticket, list_tickets, get_ticket
from campusflow.workflow import assign_ticket, change_status, work_queue
from campusflow.reports import show_report
from campusflow.storage import load_tickets, save_tickets

DATA_FILE = "data/tickets.json"


def ask_number(prompt):
    """Ask for a whole number and repeat until the user enters one."""
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a whole number.")


def main():
    try:
        tickets = load_tickets(DATA_FILE)
    except (ValueError, OSError) as error:
        print(f"Could not load saved tickets: {error}")
        return

    while True:
        print("""
=== CampusFlow Helpdesk ===
1. Create ticket
2. List all tickets
3. View one ticket
4. Assign ticket
5. Change ticket status
6. Show work queue
7. Show reports
0. Exit
""")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                title = input("Title: ")
                category = input("Category (Network/Hardware/Software/Other): ")
                urgency = input("Urgency (low/medium/high): ")
                affected = ask_number("Number of affected users: ")
                ticket = create_ticket(tickets, title, category, urgency, affected)
                save_tickets(DATA_FILE, tickets)
                print("Created:", ticket)

            elif choice == "2":
                list_tickets(tickets)

            elif choice == "3":
                ticket_id = input("Ticket ID (e.g. T001): ").strip().upper()
                print(get_ticket(tickets, ticket_id))

            elif choice == "4":
                ticket_id = input("Ticket ID: ").strip().upper()
                staff = input("Assign to staff member: ")
                assign_ticket(tickets, ticket_id, staff)
                save_tickets(DATA_FILE, tickets)
                print("Ticket assigned.")

            elif choice == "5":
                ticket_id = input("Ticket ID: ").strip().upper()
                status = input("New status (open/in_progress/resolved): ")
                change_status(tickets, ticket_id, status)
                save_tickets(DATA_FILE, tickets)
                print("Status updated.")

            elif choice == "6":
                for ticket in work_queue(tickets):
                    print(ticket)

            elif choice == "7":
                show_report(tickets)

            elif choice == "0":
                save_tickets(DATA_FILE, tickets)
                print("Goodbye!")
                break

            else:
                print("Invalid menu option.")

        except (ValueError, KeyError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
