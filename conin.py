import pandas as pd
from datetime import datetime

# Load the CSV file
csv_file = 'inquiry.csv'
df = pd.read_csv(csv_file)

# Convert Unix timestamps to '%Y-%m-%d' format
df['db'] = pd.to_datetime(df['db'], unit='s').dt.strftime('%Y-%m-%d')
df['model'] = pd.to_datetime(df['model'], unit='s').dt.strftime('%Y-%m-%d')

# Save changes to the same file (overwrite)
df.to_csv(csv_file, index=False)

print("Date conversion completed successfully.")
