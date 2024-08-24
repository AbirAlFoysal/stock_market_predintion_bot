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
        df = pd.read_csv(os.path.join(directory, filename))

        # Check if 'timestamp' column exists and is not empty
        if 'timestamp' in df.columns and not df['timestamp'].empty:
            # Get the last value of the "timestamp" column
            last_timestamp = df['timestamp'].iloc[-1]

            # Append the file information to the list
            data.append({'share': filename.replace(".csv",""), 'db': last_timestamp, 'model': ''})

# Create a new DataFrame
inquiry_df = pd.DataFrame(data, columns=['share', 'db', 'model'])

# Save the DataFrame to a new CSV file
inquiry_df.to_csv('inquiry.csv', index=False)

print("inquiry.csv created successfully.")
