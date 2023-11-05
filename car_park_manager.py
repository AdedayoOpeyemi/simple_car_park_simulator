import os
import csv
import re
import datetime
from datetime import datetime

CSV_FILENAME = "parking_records.csv"
HOURLY_RATE = 2
ALL_PARKING_SPOTS = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
AVAILABLE_SPOTS = []
csv_headers = ["Ticket Id", "Vehicle Reg no", "Parking spot", "Entry Time", "Exit Time", "Parking fee", "Status"]
header_mapping = {"ticket_number": "Ticket Id",
                  "car_reg_no": "Vehicle Reg no",
                  "parking_spot": "Parking spot",
                  "entry_time": "Entry Time",
                  "exit_time": "Exit Time",
                  "parking_fee": "Parking fee",
                  "status": "Status"
                  }

def initialize():

    # csv_filename = "parking_records.csv"
    if not os.path.isfile(CSV_FILENAME):
        # If the CSV file doesn't exist, create it with headers
        with open(CSV_FILENAME, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            headers = ["Ticket Id", "Vehicle Reg no", "Parking spot", "Entry Time", "Exit Time", "Parking fee", "Status"]
            csv_writer.writerow(headers)
    
    # update available car park spots
    update_available_spots()

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
    assigned_parking_spot = extract_open_parking_spots(CSV_FILENAME)[0]
    # Get the entry time (current time)
    # entry_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time_epoch))

    # Initialize exit time and parking fee to None
    exit_time = None
    parking_fee = None

    # Create a dictionary to store the ticket record
    ticket_record = {
        "ticket_number": ticket_number,
        "car_reg_number": car_reg_number,
        "parking_spot": assigned_parking_spot,
        "entry_time": entry_time,
        "exit_time": exit_time,
        "parking_fee": parking_fee,
        "status": "open"
        # "special_time": entry_time.strftime('%a, %d %b %Y %H:%M:%S')
        # "special_time":datetime.utcfromtimestamp(entry_time).strftime('%a, %d %b %Y %H:%M:%S')
    }

    return ticket_record

def map_ticket_record_to_headers(ticket_record):
    mapped_record = {
        "Ticket Id": ticket_record.get("ticket_number", ""),
        "Vehicle Reg no": ticket_record.get("car_reg_number", ""),
        "Parking spot": ticket_record.get("parking_spot", ""),
        "Entry Time": ticket_record.get("entry_time", ""),
        "Exit Time": ticket_record.get("exit_time", ""),
        "Parking fee": ticket_record.get("parking_fee", ""),
        "Status": ticket_record.get("status", "")
    }
    return mapped_record

# def save_ticket_record(ticket_record, filename=CSV_FILENAME):
#     with open(filename, 'a', newline='') as csvfile:
#         csv_writer = csv.writer(csvfile)
#         row = [
#             ticket_record["ticket_number"],
#             ticket_record["car_reg_number"],
#             ticket_record["parking_spot"],
#             ticket_record["entry_time"],
#             ticket_record["exit_time"],
#             ticket_record["parking_fee"],
#             ticket_record["status"]
#         ]
#         csv_writer.writerow(row)
#         print("New ticket saved")

def save_ticket_record(ticket_record, filename=CSV_FILENAME):
    mapped_record = map_ticket_record_to_headers(ticket_record)
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        # csv_writer.writeheader()
        csv_writer.writerow(mapped_record)
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
                    # "human_readable": exit_time_human
                }

    return None 


def extract_open_parking_spots(csv_file=CSV_FILENAME):
    closed_parking_spots = []
    
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row['Status'] == 'open':
                closed_parking_spots.append(row['Parking spot'])

    available_spots = [spot for spot in ALL_PARKING_SPOTS if spot not in closed_parking_spots]

    return available_spots

def update_available_spots():
    AVAILABLE_SPOTS = extract_open_parking_spots(CSV_FILENAME)

def close_ticket(car_reg):
    update_exit_time(car_reg)
    # update_parking_fee(car_reg)
    # update_ticket_status()
# print(extract_open_parking_spots(CSV_FILENAME))

# def update_exit_time():


# def update_exit_time(car_reg, csv_file=CSV_FILENAME):
#     # Get the current date and time
#     exit_time = int(datetime.now().timestamp())

#     # Read the original CSV file and create a temporary list to store the updated data
#     updated_data = []

#     with open(csv_file, 'r') as csvfile:
#         csv_reader = csv.reader(csvfile)
#         # header = next(csv_reader)  # Skip the header row
#         # updated_data.append(header)  # Add the header to the updated data
#         csv_reader = csv.DictReader(csvfile)  # Create a DictReader object
#         for row in csv_reader:
#             if row['Vehicle Reg no'] == car_reg and row['Status'] == 'open':
#             # if row[1] == car_reg:
#                 # Update the "Exit Time" field with the current time
#                 row['exit_time'] = exit_time
#             updated_data.append(row)

#     # Write the modified data back to the same CSV file while maintaining the entry order
#     with open(csv_file, 'w', newline='') as csvfile:
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerows(updated_data)


def update_exit_time(car_reg, csv_file=CSV_FILENAME):
    # Get the current date and time
    exit_time = int(datetime.now().timestamp())

    # Read the original CSV file and create a temporary list to store the updated data
    updated_data = []

    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)  # Create a DictReader object
        for row in csv_reader:
            if row['Vehicle Reg no'] == car_reg and row['Status'] == 'open':
                # Update the "Exit Time" field with the current time
                row['Exit Time'] = exit_time
                row['Status'] = 'Closed'
            updated_data.append(row)

    # Write the updated data back to the CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = csv_reader.fieldnames
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()  # Write the header row
        csv_writer.writerows(updated_data)

    print(f"Exit time updated for vehicle with registration number {car_reg}")

def update_parking_fee(car_reg):
    parking_fee = calculate_fee(car_reg)

def calculate_fee(car_reg):
    print("I will calculate the fee")
