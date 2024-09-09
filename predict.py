import numpy as np
import pandas as pd
import joblib
from datetime import timedelta
import json

def load_model_and_predict(model_name, days=1):
    model_path = f'allmodels/{model_name}.pkl'
    
    try:
        dataset = pd.read_csv(f'./DB_csv/unadjusted_amarstock/{model_name}.csv')

        if 'adj_close' not in dataset.columns or len(dataset) < 15:
            raise ValueError("The dataset must contain at least 15 adj_close values for prediction.")
        
        last_values = dataset['adj_close'].tail(60).values
        
        if len(last_values) < 60:
            last_values = dataset['adj_close'].tail(30).values
            if len(last_values) < 30:
                last_values = dataset['adj_close'].tail(15).values
        
        try:
            model = joblib.load(model_path)
        except Exception as e:
            raise ValueError(f"Error loading model: {e}")
        
        predictions = []

        for i in range(days):
            try:
                next_value = model.predict([last_values[-3:]])[0]
            except Exception as e:
                raise ValueError(f"Error during prediction: {e}")
            
            predictions.append(next_value)
            
            last_values = np.append(last_values, next_value)[-60:]  # Keep only the last 60 values

        last_date = pd.to_datetime(dataset['timestamp'].iloc[-1])
        prediction_dates = [last_date + timedelta(days=i+1) for i in range(days)]

        percentage_changes = [0] + [
            ((predictions[j] - predictions[j-1]) / predictions[j-1]) * 100 for j in range(1, len(predictions))
        ]

        predictions_dict = {
            date.strftime('%Y-%m-%d'): {
                'predicted_value': format(pred, '.12f'),  # Maintain 12 decimal places
                'percentage_change': format(change, '.12f')  # Maintain 12 decimal places
            }
            for date, pred, change in zip(prediction_dates, predictions, percentage_changes)
        }

        print(json.dumps(predictions_dict, indent=4))
        return json.dumps(predictions_dict)

    except FileNotFoundError as e:
        return json.dumps({"error": f"File not found: {e}"})
    except joblib.externals.loky.process_executor._RemoteTraceback as e:
        return json.dumps({"error": f"Model loading error: {e}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

# model_name = 'PTL'
# days = 7
# load_model_and_predict(model_name, days)
