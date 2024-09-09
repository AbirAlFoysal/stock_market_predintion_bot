import numpy as np
import pandas as pd
import joblib
from datetime import timedelta
import json
from retrain import retrain_model  # Replace 'your_module_name' with the actual module name

def load_model_and_predict(model_name, days=7):
    model_path = f'allmodels/{model_name}.pkl'
    try:
        # Load the dataset
        dataset = pd.read_csv(f'./DB_csv/unadjusted_amarstock/{model_name}.csv')

        # Feature engineering
        dataset['Increase_Decrease'] = np.where(dataset['volume'].shift(-1) > dataset['volume'], 1, 0)
        dataset['Buy_Sell_on_Open'] = np.where(dataset['opening'].shift(-1) > dataset['opening'], 1, 0)
        dataset['Buy_Sell'] = np.where(dataset['adj_close'].shift(-1) > dataset['adj_close'], 1, 0)
        dataset['Returns'] = dataset['adj_close'].pct_change()
        dataset = dataset.dropna()

        # Load the initial model
        model = joblib.load(model_path)

        # Prepare to store predictions
        predictions = []
        last_data = dataset[['opening', 'high', 'low', 'volume']].values[-1].reshape(1, -1)

        # Predict in batches of 5
        for i in range(0, days, 5):
            batch_size = min(5, days - i)
            temp_predictions = []

            for _ in range(batch_size):
                pred = model.predict(last_data)
                temp_predictions.append(pred[0])
                last_data = np.append(last_data[:, 1:], pred).reshape(1, -1)
            
            predictions.extend(temp_predictions)

            # Retrain model with new predictions added to the training data
            new_data = {
                'timestamp': pd.to_datetime(dataset['timestamp'].iloc[-1]) + timedelta(days=i+1),
                'opening': last_data[0][0],
                'high': last_data[0][1],
                'low': last_data[0][2],
                'adj_close': temp_predictions[-1],
                'volume': last_data[0][3],
            }

            model = retrain_model(model_name, additional_data=[new_data])

        # Generate dates for the predictions
        last_date = pd.to_datetime(dataset['timestamp'].iloc[-1])
        prediction_dates = [last_date + timedelta(days=i+1) for i in range(days)]

        # Calculate the percentage change
        percentage_changes = []
        for j in range(1, len(predictions)):
            percentage_change = ((predictions[j] - predictions[j-1]) / predictions[j-1]) * 100
            percentage_changes.append(percentage_change)

        # The first day won't have a percentage change since there's no previous day to compare to
        percentage_changes.insert(0, 0)

        # Create a dictionary with dates as keys and predictions and percentage changes as values
        predictions_dict = {
            date.strftime('%Y-%m-%d'): {
                'predicted_value': round(pred, 2),
                'percentage_change': round(change, 2)
            }
            for date, pred, change in zip(prediction_dates, predictions, percentage_changes)
        }

        # Convert the dictionary to JSON
        print(json.dumps(predictions_dict))
        return json.dumps(predictions_dict)

    except FileNotFoundError as e:
        return json.dumps({"error": f"File not found: {e}"})
    except joblib.externals.loky.process_executor._RemoteTraceback as e:
        return json.dumps({"error": f"Model loading error: {e}"})
    except Exception as e:
        return json.dumps({"error": str(e)})
