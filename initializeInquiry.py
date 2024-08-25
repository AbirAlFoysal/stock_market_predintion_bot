import os
import pandas as pd
from tqdm import tqdm

# Directory containing the CSV files
directory = r'D:\AbleAid\StockPradiction\DB_csv\unadjusted_amarstock'  # Replace with your directory path

# Initialize the list to store the data
data = []

# Iterate through all the files in the directory with progress bar
for filename in tqdm(os.listdir(directory), desc="Processing CSV files"):
    if filename.endswith('.csv'):
        # Read the CSV file
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)

        # Check if 'timestamp' column exists
        if 'timestamp' in df.columns:
            # Drop any NaN values and take the last non-empty value in the "timestamp" column
            last_timestamp = df['timestamp'].dropna().iloc[-1] if not df['timestamp'].dropna().empty else ''

        else:
            # If 'timestamp' column is missing, set last_timestamp to an empty string
            last_timestamp = ''
        
        # Append the file information to the list, keeping "db" column empty if last_timestamp is empty
        data.append({'share': filename.replace(".csv", ""), 'db': last_timestamp, 'model': ''})

# Create a new DataFrame
inquiry_df = pd.DataFrame(data, columns=['share', 'db', 'model'])

# Save the DataFrame to a new CSV file
inquiry_df.to_csv('inquiry.csv', index=False)

print("inquiry.csv created successfully.")
