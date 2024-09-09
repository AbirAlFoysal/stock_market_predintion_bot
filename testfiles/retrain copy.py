import os
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import joblib

def retrain_model(model_name, additional_data=None):
    csv_file = f'./DB_csv/unadjusted_amarstock/{model_name}.csv'
    model_file = f'allmodels/{model_name}.pkl'

    # Check if the file exists
    if not os.path.isfile(csv_file):
        raise FileNotFoundError(f"The file {csv_file} does not exist.")
    
    try: 
        dataset = pd.read_csv(csv_file)
        
        if len(dataset) < 2:
            raise ValueError("The dataset must contain at least 2 rows to train the model.")

        dataset['Increase_Decrease'] = np.where(dataset['volume'].shift(-1) > dataset['volume'], 1, 0)
        dataset['Buy_Sell_on_Open'] = np.where(dataset['opening'].shift(-1) > dataset['opening'], 1, 0)
        dataset['Buy_Sell'] = np.where(dataset['adj_close'].shift(-1) > dataset['adj_close'], 1, 0)
        dataset['Returns'] = dataset['adj_close'].pct_change()
        dataset = dataset.dropna()

        # Include additional data if provided
        if additional_data is not None:
            additional_df = pd.DataFrame(additional_data, columns=dataset.columns)
            dataset = pd.concat([dataset, additional_df], ignore_index=True)

        # Prepare features and target
        X = dataset[['opening', 'high', 'low', 'volume']].values
        Y = dataset['adj_close'].values

        # Ensure we have data to train on
        if len(X) == 0 or len(Y) == 0:
            raise ValueError("The dataset is empty after preprocessing. Ensure your data contains valid entries.")

        # Train the model
        gb = GradientBoostingRegressor(max_depth=4, n_estimators=50, random_state=2)
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

        # Return the trained model
        return gb

    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty or could not be read.")
    except Exception as e:
        print(f"An error occurred: {e}")
