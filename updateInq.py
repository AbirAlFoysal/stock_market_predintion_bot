import pandas as pd

def update_db_column(timestamp_value, col):
    # Load the CSV file into a DataFrame
    df = pd.read_csv("inquiry.csv")

    # Update the 'db' col where 'timestamp' matches the provided value
    df.loc[df['share'] == timestamp_value, col] = "new_db_value"
    
    # Save the updated DataFrame back to the CSV file
    # df.to_csv(csv_file, index=False)

    print(f"Updated 'db' column where 'timestamp' equals '{timestamp_value}' to '{col}'.")
