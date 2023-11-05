from car_park_manager import *

def main():
    initialize()
    print("Welcome to the Best and safest car park in the world")

    while True:
        display_menu()
        choice = get_user_choice()
        if choice == 1:
            # Handle option 1: Enter the car park
            print("======================================================")
            print("enter_car_park()")
            print("======================================================")
            enter_car_park()
        elif choice == 2:
            # Handle option 2: Exit the car park
            print("exit_car_park()")
            print("======================================================")
            exit_car_park()
        elif choice == 3:
            # Handle option 3: Query parking record by ticket number
            print("query_parking_record()")
            print("======================================================")
            get_ticket_details()
        elif choice == 4:
            # Handle option 4: Quit
            print("Goodbye!")
            print("======================================================")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            print("======================================================")

    

def display_menu():
    display_available_space()
    print("You can choose of of the following options from the menu below:")
    print("1. Enter the car park")
    print("2. Exit the car park")
    print("3. Query parking record by ticket number")
    print("4. Quit")
    print("======================================================")

def get_user_choice():
    while True:
        try:
            choice = int(input("Please enter your choice: "))
            return choice
        except ValueError:
            print("Invalid input. only integers are permitted.")

def enter_car_park():
    while True:
        car_reg = get_car_reg()
        if is_valid_uk_registration(car_reg):
            print("The car reg is valid")
            ticket = create_ticket(car_reg)
            print(ticket)
            save_ticket_record(ticket)
            break
        else:
            print("Invalid car registration number. Please enter a valid UK car registration number.")

def get_car_reg():
    car_reg = input("Please enter your car reg: ")
    return(car_reg)

def get_ticket_details():
    ticket_number = input("Please enter your ticket number: ")
    
    ticket_details = fetch_ticket_details_from_csv(ticket_number)
    # print(ticket_details)

    if ticket_details:
        print(ticket_details)
    else:
        print("Ticket with number not found, please check that you are putting in the correct information")

def display_available_space():
    print(f"There are {len(extract_open_parking_spots())} spots available")

    # print("There are {extract_open_parking_spots()} spots available")

def exit_car_park():
    car_reg=input("Please enter your car reg number: ")
    close_ticket(car_reg)
    # display_ticket()

if __name__ == "__main__":
    main()