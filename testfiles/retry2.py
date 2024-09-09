import joblib
import pandas as pd
import numpy as np

def predict_next_values_from_dataset(model_name, csv_file, n_predictions=3):
    model_file = f'{model_name}.pkl'

    # Load the dataset
    dataset = pd.read_csv(csv_file)

    # Extract the last 60 values of adj_close
    last_60_values = dataset['adj_close'].tail(60).values

    if len(last_60_values) < 60:
        raise ValueError("The dataset must contain at least 60 adj_close values for prediction.")

    try:
        # Load the trained model
        gb = joblib.load(model_file)

        predictions = []
        last_values = last_60_values[-3:]  # Take the last 3 values to start predictions
        for _ in range(n_predictions):
            # Predict the next value using the model
            next_value = gb.predict([last_values])[0]
            predictions.append(next_value)

            # Shift the last values and append the new predicted value
            last_values = [next_value] + list(last_values[:-1])

        return predictions

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Assuming the model has already been trained and saved
csv_file = './DB_csv/unadjusted_amarstock/PTL.csv'
next_values = predict_next_values_from_dataset('PTL', csv_file)
print("Next 3 predicted values of adj_close:", next_values)
