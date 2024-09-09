import numpy as np
import pandas as pd
import joblib
from datetime import timedelta
import json
from retrain import retrain_model  # Replace with the actual module name

def load_model_and_predict(model_name, days=1):
    model_path = f'allmodels/{model_name}.pkl'
    
    try:
        # Load the dataset
        dataset = pd.read_csv(f'./DB_csv/unadjusted_amarstock/{model_name}.csv')

        # Ensure the dataset has enough rows
        if 'adj_close' not in dataset.columns or len(dataset) < 15:
            raise ValueError("The dataset must contain at least 15 adj_close values for prediction.")
        
        # Extract the last 60 values of adj_close for prediction
        last_60_values = dataset['adj_close'].tail(60).values
        
        # Fallback to smaller datasets if fewer rows are available
        if len(last_60_values) < 60:
            last_60_values = dataset['adj_close'].tail(30).values
            if len(last_60_values) < 30:
                last_60_values = dataset['adj_close'].tail(15).values

        # Load the initial model
        try:
            model = joblib.load(model_path)
        except Exception as e:
            raise ValueError(f"Error loading model: {e}")
        
        # Prepare to store predictions
        predictions = []
        last_values = last_60_values[-3:]  # Start with the last 3 adj_close values

        # Predict in batches
        for i in range(days):
            try:
                next_value = model.predict([last_values])[0]
            except Exception as e:
                raise ValueError(f"Error during prediction: {e}")
            
            predictions.append(next_value)
            last_values = [next_value] + list(last_values[:-1])  # Update last values

            # Retrain model with new predictions
            new_data = {
                'timestamp': pd.to_datetime(dataset['timestamp'].iloc[-1]) + timedelta(days=i+1),
                'adj_close': next_value,
            }
            try:
                model = retrain_model(model_name, additional_data=[new_data])
            except Exception as e:
                raise ValueError(f"Error during model retraining: {e}")

        # Generate dates for the predictions
        last_date = pd.to_datetime(dataset['timestamp'].iloc[-1])
        prediction_dates = [last_date + timedelta(days=i+1) for i in range(days)]

        # Calculate the percentage change
        percentage_changes = [0] + [
            ((predictions[j] - predictions[j-1]) / predictions[j-1]) * 100 for j in range(1, len(predictions))
        ]

        # Create a dictionary with dates, predictions, and percentage changes
        predictions_dict = {
            date.strftime('%Y-%m-%d'): {
                'predicted_value': format(pred, '.12f'),  # Up to 12 decimal places
                'percentage_change': format(change, '.12f')  # Up to 12 decimal places
            }
            for date, pred, change in zip(prediction_dates, predictions, percentage_changes)
        }

        # Convert to JSON and return
        print(json.dumps(predictions_dict, indent=4))
        return json.dumps(predictions_dict)

    except FileNotFoundError as e:
        return json.dumps({"error": f"File not found: {e}"})
    except joblib.externals.loky.process_executor._RemoteTraceback as e:
        return json.dumps({"error": f"Model loading error: {e}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

# Example usage
model_name = 'PTL'
days = 7
load_model_and_predict(model_name, days)

