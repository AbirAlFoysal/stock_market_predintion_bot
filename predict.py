# predict.py

import pickle
import pandas as pd
import numpy as np
import os
import json

def load_model_and_predict(sample_file, days=7):
    model_directory = "allmodels"
    sample_file = str(sample_file) + ".pkl"

    try:
        # Load the trained model
        model_file = os.path.join(model_directory, sample_file)
        
        if not os.path.exists(model_file):
            raise FileNotFoundError(f"Model file '{model_file}' not found.")
        
        with open(model_file, 'rb') as f:
            gb = pickle.load(f)
        
        print(f"Model loaded from {model_file}")
        
        # Assume the dataset to be the same as during training
        csv_directory = "./DB_csv/unadjusted_amarstock/"
        data_file = os.path.join(csv_directory, sample_file.replace('.pkl', '.csv'))
        
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file '{data_file}' not found.")
        
        df = pd.read_csv(data_file)

        # Check if the necessary columns are present
        required_columns = ['timestamp', 'opening', 'high', 'low', 'volume', 'adj_close']
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"Required column '{column}' is missing from the dataset.")

        # Compute missing columns if necessary
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['day_of_year'] = df['timestamp'].dt.dayofyear
        df['year'] = df['timestamp'].dt.year
        df['lag1'] = df['adj_close'].shift(1)
        df['lag2'] = df['adj_close'].shift(2)
        df['rolling_mean'] = df['adj_close'].rolling(window=5).mean()
        df['rolling_std'] = df['adj_close'].rolling(window=5).std()
        df = df.dropna()

        # Ensure the dataframe is not empty
        if df.empty:
            raise ValueError("The dataset is empty. Cannot proceed with prediction.")

        # Prepare the last known data
        last_known_day = df['day_of_year'].iloc[-1]
        last_known_year = df['year'].iloc[-1]
        last_row = df.iloc[-1][['opening', 'high', 'low', 'volume', 'lag1', 'lag2', 'rolling_mean', 'rolling_std']].values

        # Predict the adj_close for the next 'days' days
        future_predictions = []
        future_dates = []
        for day in range(1, days + 1):
            next_day_of_year = (last_known_day + day) % 365
            next_year = last_known_year + (last_known_day + day) // 365

            # Ensure the input features match the model's expected features
            input_features = np.array([*last_row, next_day_of_year, next_year])
            if input_features.shape[0] != gb.n_features_in_:
                raise ValueError(f"Feature count mismatch: Model expects {gb.n_features_in_} features, but got {input_features.shape[0]}.")

            # Make the prediction
            prediction = gb.predict([input_features])[0]
            future_predictions.append(prediction)
            
            # Calculate future date
            last_date = df['timestamp'].iloc[-1]
            future_date = last_date + pd.DateOffset(days=day)
            future_dates.append(future_date.strftime('%Y-%m-%d'))

        # Create a dictionary of predictions
        predictions_dict = dict(zip(future_dates, future_predictions))
        
        # Convert the dictionary to JSON
        predictions_json = json.dumps(predictions_dict, indent=4)
        
        print(f"Predicted adj_close prices for the next {days} days:")
        print(predictions_json)

        return predictions_json

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
    except ValueError as val_error:
        print(f"Error: {val_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
