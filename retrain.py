import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error as MSE

def retrain_model(csv_file, model_file):
    # Load the CSV file
    df = pd.read_csv(csv_file)

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

            # Delete the previous model if it exists
            if os.path.exists(model_file):
                os.remove(model_file)

            # Save the new model
            joblib.dump(gb, model_file)

            print(f"Model trained and saved as {model_file}. RMSE: {rmse:.4f}")

# Example usage:
# csv_file = r'D:\AbleAid\StockPradiction\DB_csv\unadjusted_amarstock\example.csv'
# model_file = r'D:\AbleAid\StockPradiction\models\example.pkl'
# train_and_replace_model(csv_file, model_file)
