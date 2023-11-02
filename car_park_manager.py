import re
import datetime
from datetime import datetime
# from time import gmtime, strftime

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