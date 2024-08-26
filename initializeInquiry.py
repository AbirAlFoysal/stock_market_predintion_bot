import os
import pandas as pd
from tqdm import tqdm

directory = r'D:\AbleAid\StockPradiction\DB_csv\unadjusted_amarstock' 

data = []

for filename in tqdm(os.listdir(directory), desc="Processing CSV files"):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        if 'timestamp' in df.columns:
            last_timestamp = df['timestamp'].dropna().iloc[-1] if not df['timestamp'].dropna().empty else ''

        else:
            last_timestamp = ''
        
        data.append({'share': filename.replace(".csv", ""), 'db': last_timestamp, 'model': ''})

inquiry_df = pd.DataFrame(data, columns=['share', 'db', 'model'])

inquiry_df.to_csv('inquiry.csv', index=False)

print("inquiry.csv created successfully.")
