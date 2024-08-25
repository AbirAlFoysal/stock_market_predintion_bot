import csv
from datetime import datetime

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
    """
    Converts a date string (e.g., "2024-02-01") to a datetime object 
    in the '%Y-%m-%d %H:%M:%S' format with default time as '00:00:01'.
    """
    return datetime.strptime(date_str + " 00:00:01", '%Y-%m-%d %H:%M:%S')

# Example usage:
stock = "ACI"
col = "db"
date_str = get_value_from_csv(stock, col)
if date_str:
    datetime_obj = convert_date_to_datetime(date_str)
    print("Converted datetime:", datetime_obj)
else:
    print("No date found.")

print(type(date_str))