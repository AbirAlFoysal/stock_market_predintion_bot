import os
import numpy as np
import pandas as pd
import joblib
from tqdm import tqdm
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error as MSE

# Directory containing the CSV files
csv_directory = r'D:\AbleAid\StockPradiction\DB_csv\unadjusted_amarstock'

# Directory to save the models
model_directory = r'D:\AbleAid\StockPradiction\models'

# Create the model directory if it doesn't exist
if not os.path.exists(model_directory):
    os.makedirs(model_directory)

inquiry_csv_path = 'inquiry.csv'

# Load the existing inquiry.csv file
if os.path.exists(inquiry_csv_path):
    inquiry_df = pd.read_csv(inquiry_csv_path)
else:
    inquiry_df = pd.DataFrame(columns=['share', 'db', 'model', 'rmse', 'points'])

# Iterate through all the files in the CSV directory with a progress bar
for filename in tqdm(os.listdir(csv_directory), desc="Processing CSV files"):
    if filename.endswith('.csv'):
        # Read the CSV file
        file_path = os.path.join(csv_directory, filename)
        df = pd.read_csv(file_path)

        # Only proceed if the file has more than 2 rows
        if len(df) > 2:
            # Check if the required columns exist
            if all(col in df.columns for col in ['volume', 'opening', 'high', 'low', 'adj_close']):
                # Prepare the dataset
                df['Increase_Decrease'] = np.where(df['volume'].shift(-1) > df['volume'], 1, 0)
                df['Buy_Sell_on_Open'] = np.where(df['opening'].shift(-1) > df['opening'], 1, 0)
                df['Buy_Sell'] = np.where(df['adj_close'].shift(-1) > df['adj_close'], 1, 0)
                df['Returns'] = df['adj_close'].pct_change()
                df = df.dropna()

                X = df[['opening', 'high', 'low', 'volume']].values
                Y = df['adj_close'].values

                # Train the model using the entire dataset
                gb = GradientBoostingRegressor(max_depth=4, n_estimators=200, random_state=2)
                gb.fit(X, Y)

                # Predict using the trained model
                y_pred = gb.predict(X)

                # Compute RMSE
                mse = MSE(Y, y_pred)
                rmse = mse ** 0.5

                # Save the model in the "models" directory with the same name as the CSV file
                model_filename = os.path.join(model_directory, filename.replace(".csv", ".pkl"))
                joblib.dump(gb, model_filename)

                # Get the last non-empty date from the 'timestamp' column
                last_date = df['timestamp'].dropna().iloc[-1]

                # Update the inquiry DataFrame
                total_points = len(df['timestamp'])
                inquiry_df.loc[inquiry_df['share'] == filename.replace(".csv", ""), 'model'] = str(last_date)
                inquiry_df.loc[inquiry_df['share'] == filename.replace(".csv", ""), 'rmse'] = rmse
                inquiry_df.loc[inquiry_df['share'] == filename.replace(".csv", ""), 'points'] = total_points
            else:
                # Add a row with the filename and empty spaces for missing data
                new_row = pd.DataFrame([{
                    'share': filename.replace(".csv", ""), 
                    'db': '',
                    'model': '',
                    'rmse': '',
                    'points': ''
                }])
                inquiry_df = pd.concat([inquiry_df, new_row], ignore_index=True)
        else:
            # Add a row with the filename and empty spaces for missing data
            new_row = pd.DataFrame([{
                'share': filename.replace(".csv", ""), 
                'db': '',
                'model': '',
                'rmse': '',
                'points': ''
            }])
            inquiry_df = pd.concat([inquiry_df, new_row], ignore_index=True)

# Save the updated inquiry.csv file
inquiry_df.to_csv(inquiry_csv_path, index=False)

print("Models trained, saved in 'models' directory, and inquiry.csv updated successfully.")
