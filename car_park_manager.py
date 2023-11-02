import os
import csv
import re
import datetime
from datetime import datetime

CSV_FILENAME = "parking_records.csv"
HOURLY_RATE = 2

def initialize():
    # csv_filename = "parking_records.csv"

    if not os.path.isfile(CSV_FILENAME):
        # If the CSV file doesn't exist, create it with headers
        with open(CSV_FILENAME, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            headers = ["Ticket Id", "Date", "License Plate", "Entry Time", "Exit Time", "Parking fee"]
            csv_writer.writerow(headers)

def is_valid_uk_registration(input_str):
    # Define a regular expression pattern to match common UK registration formats
    patterns = [
        r'^[A-Z]{2}\d{2} [A-Z]{3}$',       # Current Standard Format
        r'^[A-Z]{3} \d{3}$',              # Dateless Personalized Plates
        r'^[A-Z]{2} \d{4}$',              # Northern Ireland Format
        r'^\d{3} [A-Z] \d{3}$',          # Diplomatic Plates
        # Add more patterns for special cases as needed
    ]

    # Use re.match() to check if the input matches any of the patterns
    for pattern in patterns:
        if re.match(pattern, input_str):
            return True
    return False


def create_ticket(car_reg_number):
    entry_time = int(datetime.now().timestamp())
    # Get the current date time in epoch format
    # current_time_epoch = int(datetime.time())
    current_time_epoch = int(datetime.now().timestamp())

    # Create a unique ticket number using car reg number and current time
    ticket_number = f"{car_reg_number}{entry_time}"

    # Get the entry time (current time)
    # entry_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time_epoch))

    # Initialize exit time and parking fee to None
    exit_time = None
    parking_fee = None

    # Create a dictionary to store the ticket record
    ticket_record = {
        "ticket_number": ticket_number,
        "car_reg_number": car_reg_number,
        "entry_time": entry_time,
        "exit_time": exit_time,
        "parking_fee": parking_fee,
        # "special_time": entry_time.strftime('%a, %d %b %Y %H:%M:%S')
        # "special_time":datetime.utcfromtimestamp(entry_time).strftime('%a, %d %b %Y %H:%M:%S')
    }

    return ticket_record

def save_ticket_record(ticket_record, filename=CSV_FILENAME):
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        row = [
            ticket_record["ticket_number"],
            ticket_record["car_reg_number"],
            ticket_record["entry_time"],
            ticket_record["exit_time"],
            ticket_record["parking_fee"]
        ]
        csv_writer.writerow(row)
        print("New ticket saved")
# def update_exit_time():


# def calculate_parking_fee(record):
#     duration = entry_time - exit_time

def fetch_ticket_details_from_csv(ticket_number):
    with open(CSV_FILENAME, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        # Skip the header row if present
        next(csv_reader, None)

        for row in csv_reader:
            print(row)
            # if len(row) >= 5:
            current_ticket_number = str(row[0])
            # print(current_ticket_number)
            # print(ticket_number)

            # Check if the current ticket number matches the desired ticket number
            if str(current_ticket_number) == ticket_number:
                print("ticket number matches")
                car_reg_number = row[1]
                # entry_time = datetime.strptime(row[2], '%H:%M:%S')
                entry_time = row[2]
                exit_time = row[3]
                parking_fee = row[4]
                # Set exit_time to None if it's empty or "None" in the CSV
                # exit_time_human = datetime.strptime(datetime.now(), '%H:%M:%S')

                # Return the ticket details
                return {
                    "ticket_number": current_ticket_number,
                    "car_reg_number": car_reg_number,
                    "entry_time": entry_time,
                    "exit_time": exit_time,
                    "parking_fee": parking_fee,
                    "human_readable": exit_time_human
                }

    return None 
