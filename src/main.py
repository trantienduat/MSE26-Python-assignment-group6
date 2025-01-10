# main.py
import sys
from db_connection import DatabaseConnection
from controllers.trip_controller import TripController
from controllers.ticket_controller import TicketController
from controllers.customer_controller import CustomerController

class BusTicketBookingSystem:
    def __init__(self):
        self.db_connection = DatabaseConnection('bus_ticket_booking.db')
        self.trip_controller = TripController(self.db_connection)
        self.ticket_controller = TicketController(self.db_connection)
        self.customer_controller = CustomerController(self.db_connection)


if __name__ == "__main__":
    
    db_connection = DatabaseConnection()
    
    app = BusTicketBookingSystem()
    while True:
        print("\n\nBus Ticket Booking System")
        print("1. Manage Trips")
        print("2. Book Ticket")
        print("3. Check Seat Availability")
        print("4. Cancel Ticket")
        print("5. Manage Customers")
        print("6. Exit")

        main_choice = input("Select an option: ")

        if main_choice == '1':
            while True:
                print("===== Manage Trips =====")
                print("\t1. Create")
                print("\t2. Delete")
                print("\t3. Back to main menu")

                sub_choice = input("Select an option: ")
                if sub_choice == '1':
                    print(f"perform create trips")
                elif sub_choice == '2':
                    pass
                elif sub_choice == '3':
                    break
                else:
                    print("Invalid option. Please try again.")

        elif main_choice == '2':
            # Book ticket logic here
            pass
        elif main_choice == '3':
            # Check seat availability logic here
            pass
        elif main_choice == '4':
            # Cancel ticket logic here
            pass
        elif main_choice == '5':
            # Manage customers logic here
            pass
        elif main_choice == '6':
            print("Exiting the application.")
            sys.exit()
        else:
            print("Invalid option. Please try again.")


