import os
import csv
import re
import datetime
from datetime import datetime

CSV_FILENAME = "parking_records.csv"
HOURLY_RATE = 2
ALL_PARKING_SPOTS = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
AVAILABLE_SPOTS = []
BASE_FEE = 0.25
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

    # Define a regular expression pattern to match common UK registration formats
    patterns = [
        r'^[A-Z]{2}\d{2} [A-Z]{3}$',       # Current Standard Format with space
        r'^[A-Z]{2}\d{2}[A-Z]{3}$',        # Current Standard Format without space
        r'^[A-Z]{3} \d{3}$',              # Dateless Personalized Plates with space
        r'^[A-Z]{3}\d{3}$',               # Dateless Personalized Plates without space
        r'^[A-Z]{2} \d{4}$',              # Northern Ireland Format with space
        r'^[A-Z]{2}\d{4}$',               # Northern Ireland Format without space
        r'^\d{3} [A-Z] \d{3}$',          # Diplomatic Plates with space
        r'^\d{3}[A-Z]\d{3}$',            # Diplomatic Plates without space
        # Add more patterns for special cases as needed
    ]

    

    # Use re.match() to check if the input matches any of the patterns
    for pattern in patterns:
        if re.match(pattern, input_str):
            return True
    return False

def create_ticket(car_reg_number):
    # Get the current date time in epoch format
    entry_time = int(datetime.now().timestamp())

    # Create a unique ticket number using car reg number and current time
    ticket_number = f"{entry_time}{car_reg_number}"
    assigned_parking_spot = extract_open_parking_spots(CSV_FILENAME)[0]

    # Initialize exit time and parking fee to None
    exit_time = None
    parking_fee = None

    # Create a dictionary to store the ticket record
    ticket_record = {
        "ticket_number": ticket_number,
        "car_reg_no": car_reg_number,
        "parking_spot": assigned_parking_spot,
        "entry_time": entry_time,
        "exit_time": exit_time,
        "parking_fee": parking_fee,
        "status": "open"
    }
    save_ticket_record(ticket_record)
    return ticket_record

def map_ticket_record_to_headers(ticket_record):
    mapped_record = {
        "Ticket Id": ticket_record.get("ticket_number", ""),
        "Vehicle Reg no": ticket_record.get("car_reg_no", ""),
        "Parking spot": ticket_record.get("parking_spot", ""),
        "Entry Time": ticket_record.get("entry_time", ""),
        "Exit Time": ticket_record.get("exit_time", ""),
        "Parking fee": ticket_record.get("parking_fee", ""),
        "Status": ticket_record.get("status", "")
    }
    return mapped_record

def save_ticket_record(ticket_record, filename=CSV_FILENAME):
    mapped_record = map_ticket_record_to_headers(ticket_record)
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        # csv_writer.writeheader()
        csv_writer.writerow(mapped_record)

def fetch_ticket_details_from_csv(ticket_number):
    ticket_details = {key: None for key in header_mapping}

    with open(CSV_FILENAME, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile, fieldnames=csv_headers)

        for row in csv_reader:
            current_ticket_number = row.get(header_mapping["ticket_number"])

            # Check if the current ticket number matches the desired ticket number
            if current_ticket_number == ticket_number:
                for key, csv_field in header_mapping.items():
                    ticket_details[key] = row.get(csv_field)
                    print(ticket_details)

                break  # Exit the loop once a matching ticket is found

    return ticket_details

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
                row['Parking fee'] = calculate_fee(int(exit_time), int(row['Entry Time']))

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

def calculate_fee(exit_time, entry_time):
    # Read the CSV file and find the entry and exit times based on the ticket number
    # entry_time = None
    # exit_time = None

    # with open(csv_file, 'r') as csvfile:
    #     csv_reader = csv.DictReader(csvfile)
    #     for row in csv_reader:
    #         if row['Vehicle Reg no'] == car_reg and row['Status'] == 'Closed':
    #             entry_time = int(row['Entry Time'])
    #             exit_time = int(row['Exit Time'])
    #             break

    # if entry_time is None or exit_time is None:
    #     print(f"Entry and exit times not found for vehicle with registration number {car_reg}")
    #     return None

    hours_parked = (exit_time - entry_time) / 3600  # Calculate hours parked
    fee = hours_parked * HOURLY_RATE  # Calculate the fee based on hours and hourly rate
    fee = round(fee, 2)
    return max(fee, BASE_FEE)
