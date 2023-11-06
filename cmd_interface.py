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

# def display_ticket(ticket):
    # if ticket:
    #     table = texttable.Texttable()
    #     table.set_cols_align(["l", "l"])
    #     table.set_cols_valign(["m", "m"])

    #     table.header(["Attribute", "Value"])
    #     table.add_row(["Ticket Number", ticket.ticket_number])
    #     table.add_row(["Car Registration Number", ticket.car_reg_number])
    #     table.add_row(["Parking Spot", ticket.parking_spot])
    #     table.add_row(["Entry Time", datetime.utcfromtimestamp(ticket.entry_time).strftime('%Y-%m-%d %H:%M:%S')])
    #     table.add_row(["Exit Time", datetime.utcfromtimestamp(ticket.exit_time).strftime('%Y-%m-%d %H:%M:%S') if ticket.exit_time else "Vehicle still parked..."])
    #     table.add_row(["Parking Fee", f"${ticket.parking_fee:.2f}" if ticket.exit_time else "Not calculated yet"])
    #     table.add_row(["Status", ticket.status])

    #     print("\033[93m")  # Set text color to yellow
    #     print("Parking Ticket Details:")
    #     print(table.draw())
    #     print("\033[0m")  # Reset text color
    # else:
    #     print("No ticket found.")

def display_ticket(ticket):
    if ticket:
        print("\033[93m")  # Set text color to yellow
        print("Parking Ticket Details:")
        print(f"{'Field':<25}{'Content':<25}")
        print('-' * 50)

        attributes = [
            ["Ticket Number:", ticket.get("ticket_number", "")],
            ["Car Registration Number:", ticket.get("car_reg_no", "")],
            ["Parking Spot:", ticket.get("parking_spot", "")],
            ["Entry Time:", datetime.utcfromtimestamp(int(ticket.get("entry_time", 0))).strftime('%Y-%m-%d %H:%M:%S')],
            ["Exit Time:", datetime.utcfromtimestamp(int(ticket.get('exit_time', 0))).strftime('%Y-%m-%d %H:%M:%S') if ticket.get("exit_time") else f"\033[3;93mVehicle still parked...\033[0m\033[93m"],
            ["Parking Fee:", f"\033[3;93m\033[3m${(float(ticket.get('parking_fee', 0.00))):.2f}\033[0m" if ticket.get("exit_time") else f"\033[3;93mNot calculated yet\033[0m\033[93m"],
            ["Status:", f"\033[3;93m{ticket.get('status', '')}\033[0m"]
        ]

        for attribute, value in attributes:
            print(f"{attribute:<25}{value:<25}")

        print("\033[0m")  # Reset text color
    else:
        print("No ticket found.")


def get_user_choice():
    while True:
        try:
            choice = int(input("Please enter your choice: "))
            return choice
        except ValueError:
            print("Invalid input. only integers are permitted.")

def enter_car_park():
    while True:
        display_guide_statement()
        car_reg = get_car_reg()
        if is_valid_uk_registration(car_reg):
            print("The car reg is valid")
            ticket = create_ticket(car_reg)
            print(ticket)
            display_ticket(ticket)
            # save_ticket_record(ticket)
            break
        else:
            print("Invalid car registration number. Please enter a valid UK car registration number.")

def get_car_reg():
    car_reg = input("Please enter your car reg: ")
    return(car_reg.strip().replace(" ", ""))

def get_ticket_details():
    ticket_number = input("Please enter your ticket number: ")
    
    ticket_details = fetch_ticket_details_from_csv(ticket_number)
    # print(ticket_details)

    if ticket_details:
        display_ticket(ticket_details)
    else:
        print("Ticket with number not found, please check that you are putting in the correct information")

def display_available_space():
    print(f"There are {len(extract_open_parking_spots())} spots available")

    # print("There are {extract_open_parking_spots()} spots available")

def exit_car_park():
    car_reg=input("Please enter your car reg number: ")
    close_ticket(car_reg)
    # display_ticket()


# def display_guide_statement():
#     green_color = "\033[32m"
#     reset_color = "\033[0m"
    
#     print(green_color + "Welcome to the UK Car Registration Validator!" + reset_color)
#     print(green_color + "Please enter your car registration in one of the following accepted formats:" + reset_color)
#     print(green_color + "1. Current Standard Format: AB12 CDE (with space)" + reset_color)
#     print(green_color + "   or AB12CDE (without space)" + reset_color)
#     print(green_color + "2. Dateless Personalized Plates: ABC 123 (with space)" + reset_color)
#     print(green_color + "   or ABC123 (without space)" + reset_color)
#     print(green_color + "3. Northern Ireland Format: AB 1234 (with space)" + reset_color)
#     print(green_color + "   or AB1234 (without space)" + reset_color)
#     print(green_color + "4. Diplomatic Plates: 123 A 456 (with space)" + reset_color)
#     print(green_color + "   or 123A456 (without space)" + reset_color)
#     print(green_color + "You can enter your car registration in any of these formats." + reset_color)


# def display_guide_statement():
#     green_color = "\033[32m"
#     reset_color = "\033[0m"
#     # box_char = "+"  # Character for drawing the box

#     # # Define the content of the box
#     # guide_text = [
#     #     green_color + "    ",
#     #     "Please enter your car registration in any of the accepted formats:",
#     #     "1. Current Standard Format: AB12 CDE or AB12CDE",
#     #     "2. Dateless Personalized Plates: ABC 123 or ABC123",
#     #     "3. Northern Ireland Format: AB 1234 or AB1234",
#     #     "4. Diplomatic Plates: 123 A 456 or 123A456",
#     #     "    " + reset_color,
#     # ]

#     box_char = "▒"  # Character for drawing the box

#     # Define the content of the box
#     guide_text = [
#         green_color,
#         "Welcome to the UK Car Registration Validator!",
#         "Please enter your car registration in any of the accepted formats:",
#         "1. Current Standard Format: AB12 CDE or AB12CDE",
#         "2. Dateless Personalized Plates: ABC 123 or ABC123",
#         "3. Northern Ireland Format: AB 1234 or AB1234",
#         "4. Diplomatic Plates: 123 A 456 or 123A456",
#         reset_color,
#     ]

#     # Determine the width of the box
#     # box_width = max(len(line) for line in guide_text) + 4  # Add padding for the box borders
#     box_width = 100

#     # Print the top border of the box
#     print(box_char * box_width)

#     # Print the content of the box
#     for line in guide_text:
#         line = line.ljust(box_width - 4)  # Left-align the text
#         print(f"{box_char} {line} {box_char}")

#     # Print the bottom border of the box
#     print(box_char * box_width)


# def display_guide_statement():
#     green_color = "\033[32m"
#     reset_color = "\033[0m"
#     box_char = "▒"  # Character for drawing the box

#     # Define the content of the box
#     guide_text = [
#         "Welcome to the UK Car Registration Validator!",
#         "Please enter your car registration in any of the accepted formats:",
#         "1. Current Standard Format: AB12 CDE or AB12CDE",
#         "2. Dateless Personalized Plates: ABC 123 or ABC123",
#         "3. Northern Ireland Format: AB 1234 or AB1234",
#         "4. Diplomatic Plates: 123 A 456 or 123A456",
#     ]

#     # Determine the width of the box
#     box_width = max(len(line) for line in guide_text) + 4  # Add padding for the box borders

#     # Print the top border of the box
#     print(box_char * box_width)

#     # Print the content of the box
#     for line in guide_text:
#         line = green_color + line + reset_color
#         line = line.center(box_width - 4)  # Center-align the text
#         print(f"{box_char} {line} {box_char}")

#     # Print the bottom border of the box
#     print(box_char * box_width)

# def display_guide_statement():
#     green_color = "\033[32m"
#     reset_color = "\033[0m"
#     box_char = "▒"  # Character for drawing the box

#     # Define the content of the box
#     guide_text = [
#         "Welcome to the UK Car Registration Validator!",
#         "Please enter your car registration in any of the accepted formats:",
#         "1. Current Standard Format: AB12 CDE or AB12CDE",
#         "2. Dateless Personalized Plates: ABC 123 or ABC123",
#         "3. Northern Ireland Format: AB 1234 or AB1234",
#         "4. Diplomatic Plates: 123 A 456 or 123A456",
#     ]

#     # Determine the width of the box
#     box_width = max(len(line) for line in guide_text) + 2  # Add padding for the box borders

#     # Print the top border of the box
#     print(box_char * box_width)

#     # Print the content of the box
#     for line in guide_text:
#         line = line.center(box_width)  # Center-align the text
#         print(f"{box_char}{green_color} {line} {reset_color}{box_char}")

#     # Print the bottom border of the box
#     print(box_char * box_width)

def display_guide_statement():
    green_color = "\033[32m"
    reset_color = "\033[0m"
    box_char = "▒"  # Character for drawing the box

    # Define the content of the box
    guide_text = [
        "Please enter your car registration in any of the accepted formats:",
        "1. Current Standard Format: AB12 CDE or AB12CDE",
        "2. Dateless Personalized Plates: ABC 123 or ABC123",
        "3. Northern Ireland Format: AB 1234 or AB1234",
        "4. Diplomatic Plates: 123 A 456 or 123A456",
    ]

    # Determine the width of the box
    box_width = max(len(line) for line in guide_text) + 2  # Add padding for the box borders
    # box_width = 80
    # Print the top border of the box
    print(box_char * box_width)

    # Print the content of the box
    for line in guide_text:
        line = green_color + line + reset_color
        line = line.ljust(box_width)  # Left-align the text
        print(f"{box_char} {line} {box_char}")

    # Print the bottom border of the box
    print(box_char * box_width)

if __name__ == "__main__":
    main()