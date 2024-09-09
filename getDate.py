import csv
from datetime import datetime

from datetime import datetime

def convert_unix_to_date_string(unix_timestamp):
    """
    Converts a Unix timestamp to a human-readable date string.
    
    Args:
    unix_timestamp (float): The Unix timestamp to convert.
    
    Returns:
    str: The human-readable date string in the format 'YYYY-MM-DD'.
    """
    # Convert Unix timestamp to a datetime object
    dt_object = datetime.fromtimestamp(unix_timestamp)
    # Format datetime object as a date string
    date_string = dt_object.strftime('%Y-%m-%d')
    return date_string

# Example usage
timestamp = 1627754400.0
date_string = convert_unix_to_date_string(timestamp)
print(f"The date string for timestamp {timestamp} is: {date_string}")


def get_value_from_csv(stock, col, csv_file="inquiry.csv"):
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['share'] == stock:
                    return row.get(col, None) 
            return None   
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None
    except KeyError:
        print(f"Error: The column '{col}' does not exist in the CSV file.")
        return None

def convert_date_to_datetime(date_str):
    # date_str = convert_unix_to_date_string(date_str)
    """
    Converts a date string (e.g., "2024-02-01") to a datetime object 
    in the '%Y-%m-%d %H:%M:%S' format with default time as '00:00:01'.
    """
    return datetime.strptime(date_str + " 00:00:01", '%Y-%m-%d %H:%M:%S')

# Example usage:
# stock = "ACI"
# col = "db"
# date_str = get_value_from_csv(stock, col)
# if date_str:
#     datetime_obj = convert_date_to_datetime(date_str)
#     print("Converted datetime:", datetime_obj)
# else:
#     print("No date found.")

# print(type(date_str))