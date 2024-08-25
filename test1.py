import pandas as pd
import os

def append_or_create_csv(file1, file2):
    # Check if the first file exists
    if os.path.exists(file1):
        # Load the first file into a DataFrame
        df1 = pd.read_csv(file1)
        
        # Load the second file into a DataFrame
        df2 = pd.read_csv(file2)
        
        # Append the second file to the first file
        combined_df = pd.concat([df1, df2], ignore_index=True)
        
        # Save the combined DataFrame back to the first file
        combined_df.to_csv(file1, index=False)
        print(f"Appended '{file2}' to '{file1}' successfully.")
    else:
        # If the first file does not exist, copy the second file as the first file
        df2 = pd.read_csv(file2)
        df2.to_csv(file1, index=False)
        print(f"'{file1}' not found. Copied '{file2}' as '{file1}'.")

append_or_create_csv(r"C:\Users\abcwets\Desktop\codes\stock_market_predintion_bot\DB_csv_full\unadjusted_amarstock\1JANATAMF.csv",r"C:\Users\abcwets\Desktop\codes\stock_market_predintion_bot\DB_csv\unadjusted_amarstock\1JANATAMF.csv")