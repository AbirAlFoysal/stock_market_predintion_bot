import os
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import joblib

def retrain_model(model_name, additional_data=None):
    csv_file = f'./DB_csv/unadjusted_amarstock/{model_name}.csv'
    model_file = f'{model_name}.pkl'

    # Check if the file exists
    if not os.path.isfile(csv_file):
        raise FileNotFoundError(f"The file {csv_file} does not exist.")
    
    try: 
        dataset = pd.read_csv(csv_file)

        if len(dataset) < 4:
            raise ValueError("The dataset must contain at least 4 rows to train the model.")

        # Create lagged features for adj_close
        dataset['adj_close_lag1'] = dataset['adj_close'].shift(1)
        dataset['adj_close_lag2'] = dataset['adj_close'].shift(2)
        dataset['adj_close_lag3'] = dataset['adj_close'].shift(3)

        # Drop any rows with missing values due to shifting
        dataset = dataset.dropna()

        # Prepare features and target
        X = dataset[['adj_close_lag1', 'adj_close_lag2', 'adj_close_lag3']].values
        Y = dataset['adj_close'].values

        # Ensure we have data to train on
        if len(X) == 0 or len(Y) == 0:
            raise ValueError("The dataset is empty after preprocessing. Ensure your data contains valid entries.")

        # Train the model
        gb = GradientBoostingRegressor(max_depth=4, n_estimators=100, random_state=2)
        gb.fit(X, Y)

        # Save the model to disk
        model_dir = 'allmodels'
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        joblib.dump(gb, model_file)

        # Compute and print RMSE (on the same data used for training)
        y_pred = gb.predict(X)
        mse_test = ((Y - y_pred) ** 2).mean()
        rmse_test = mse_test ** (1/2)
        print(f'Training set RMSE of gb: {rmse_test:.3f}')

        return gb

    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty or could not be read.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to retrain the model
retrain_model('PTL')
