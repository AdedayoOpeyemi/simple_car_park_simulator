import re

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

