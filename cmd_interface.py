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

# def display_menu():
#     display_available_space()
#     print("You can choose of of the following options from the menu below:")
#     print("1. Enter the car park")
#     print("2. Exit the car park")
#     print("3. Query parking record by ticket number")
#     print("4. Quit")
#     print("======================================================")

# def display_menu():
#     menu_options = [
#         "1. Enter the car park",
#         "2. Exit the car park",
#         "3. Query parking record by ticket number",
#         "4. Quit"
#     ]

#     # Determine the width of the box
#     box_width = max(len(option) for option in menu_options) + 4  # Add padding for the box borders
#     box_char = "▒"  # Character for drawing the box
#     border_line = box_char * box_width  # Top and bottom borders

#     # Display the top border
#     print(border_line)

#     print("You can choose one of the following options from the menu below:")
    
#     # Display menu options with left alignment
#     for option in menu_options:
#         print(f"{box_char} {option:{box_width-4}} {box_char}")

#     # Display the bottom border
#     print(border_line)

def display_menu():
    green_cyan_color = "\033[96m"  # ANSI escape code for green-cyan text
    reset_color = "\033[0m"  # ANSI escape code to reset color
    box_char = "█"  # Character for drawing the box
    top_bottom_border = "▄"  # Character for the top and bottom borders
    side_border = "█"  # Character for the side borders

    menu_options = [
        "You can choose one of the following options from the menu below:",
        "1. Enter the car park",
        "2. Exit the car park",
        "3. Query parking record by ticket number",
        "4. Quit"
    ]

    # Determine the width of the box
    box_width = max(len(option) for option in menu_options) + 6  # Add padding for the box borders

    # Display the top border with green-cyan color
    print(green_cyan_color + top_bottom_border * box_width + reset_color)

    # Display menu options with left alignment in green-cyan color
    for option in menu_options:
        print(green_cyan_color + f"{side_border} {option:{box_width-4}} {side_border}" + reset_color)

    # Display the bottom border with green-cyan color
    print(green_cyan_color + top_bottom_border * box_width + reset_color)

def display_ticket(ticket):
    if ticket:
        print("\033[93m")  # Set text color to yellow
        print("+" + "-" * 48 + "+")  # Top border
        print("|{:<48}|".format("Parking Ticket Details"))
        print("|" + "-" * 48 + "|")  # Separator
        attributes = [
            ["Ticket Number:", ticket.get("ticket_number", "")],
            ["Car Registration Number:", ticket.get("car_reg_no", "")],
            ["Parking Spot:", ticket.get("parking_spot", "")],
            ["Entry Time:", datetime.utcfromtimestamp(int(ticket.get("entry_time", 0))).strftime('%Y-%m-%d %H:%M:%S')],
            ["Exit Time:", datetime.utcfromtimestamp(int(ticket.get('exit_time', 0))).strftime('%Y-%m-%d %H:%M:%S') if ticket.get("exit_time") else "\033[3;93mVehicle still parked...\033[0m\033[93m"],
            ["Parking Fee:", f"${(float(ticket.get('parking_fee', 0.00))):.2f}" if ticket.get("exit_time") else "\033[3;93mNot calculated yet\033[0m\033[93m"],
            ["Status:", f"{ticket.get('status', '')}"]
        ]
        for attribute, value in attributes:
            print("|{:<24}|{:<23}|".format(attribute, value))
        print("+" + "-" * 48 + "+")  # Bottom border
        print("\033[0m")  # Reset text color
    else:
        print("No ticket found.")

def get_user_choice():
    while True:
        try:
            choice = int(input("Please enter your choice: "))
            return choice
        except ValueError:
            print("\n\033[38;5;208m▒ Invalid input. Only integers between 1 - 4 are permitted. ▒\033[0m\n")

def enter_car_park():
    while True:
        if no_available_space():
            print_no_available_spaces_message()
            break
        enter_park_guide_statement()
        go_back_guide()
        car_reg = get_car_reg()
        if car_reg == "*":
            break
        if is_valid_uk_registration(car_reg):
            transaction = create_ticket(car_reg)
            if transaction['status'] == 'failed':
                print_error_message(transaction['message'])
                input("\033[93mPress Enter to retry...\033[0m")
                enter_car_park()
            else:
                display_ticket(transaction['ticket'])
            break
        else:
            print("\n\033[91mInvalid car registration number.\nPlease enter a valid UK car registration number or * to go back to the previous menu\033[0m\n")

def get_car_reg():
    car_reg = input("Please enter your car reg: ")
    return(car_reg.strip().replace(" ", ""))

def get_ticket_details():
    while True:
        go_back_guide()
        ticket_number = input("Please enter your ticket number: ")
        if ticket_number == "*":
            break
        ticket_details = fetch_ticket_details_from_csv(ticket_number)
        # print(ticket_details)

        if ticket_details:
            display_ticket(ticket_details)
        else:
            print("Ticket with number not found, please check that you are putting in the correct information")

def display_available_space():
    print(f"There are {len(extract_open_parking_spots())} spots available")

def exit_car_park():
    while True:
        go_back_guide()
        car_reg = input("Please enter your car reg number: ")
        if car_reg == "*":
            break
        ticket = close_ticket(car_reg)
        if ticket:
            display_ticket(ticket)
            break
        else:
            print("No such record found, try again")

def enter_park_guide_statement():
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
    box_width = max(len(line) for line in guide_text) + 4  # Add padding for the box borders
    # Print the top border of the box
    print(box_char * box_width)

    # Print the content of the box
    for line in guide_text:
        line = green_color + line + reset_color
        line = line.ljust(box_width + 5)  # Left-align the text with padding
        print(f"{box_char} {line} {box_char}")

    # Print the bottom border of the box
    print(box_char * box_width)

def go_back_guide():
    print("\n\033[38;5;208mPress * to go back to the previous menu\033[0m\n")

def print_no_available_spaces_message():
    orange_color = "\033[38;5;208m"  # ANSI escape code for orange color
    reset_color = "\033[0m"  # ANSI escape code to reset color

    print(orange_color + "Currently, there are no available parking spaces in the park.")
    print("Please consider trying a different parking location." + reset_color)

def print_error_message(message):
    # ANSI escape code for red color
    red_color_code = "\033[91m"
    # ANSI escape code for resetting text color
    reset_color_code = "\033[0m"

    # Combine the color code with the main message and reset the color afterward
    colored_message = f"{red_color_code}{message}{reset_color_code}"

    # Border characters and style for the error message
    border = "#" * (len(colored_message) + 4)
    style_border = f"{red_color_code}{border}{reset_color_code}"

    # Create a formatted error message with border
    formatted_error_message = f"{style_border}\n#  {colored_message}  #\n{style_border}"

    # Print the formatted error message
    print(formatted_error_message)
    
if __name__ == "__main__":
    main()