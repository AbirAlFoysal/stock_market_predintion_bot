import os
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import joblib

def retrain_model(model_name, additional_data=None):
    csv_file = f'./DB_csv/unadjusted_amarstock/{model_name}.csv'
    model_file = f'allmodels/{model_name}.pkl'  
    if not os.path.isfile(csv_file):
        raise FileNotFoundError(f"The file {csv_file} does not exist.")
    
    try: 
        dataset = pd.read_csv(csv_file)

        if len(dataset) < 4:
            raise ValueError("The dataset must contain at least 4 rows to train the model.")

        dataset['adj_close_lag1'] = dataset['adj_close'].shift(1)
        dataset['adj_close_lag2'] = dataset['adj_close'].shift(2)
        dataset['adj_close_lag3'] = dataset['adj_close'].shift(3)

        dataset = dataset.dropna()

        X = dataset[['adj_close_lag1', 'adj_close_lag2', 'adj_close_lag3']].values
        Y = dataset['adj_close'].values
        if len(X) == 0 or len(Y) == 0:
            raise ValueError("The dataset is empty after preprocessing. Ensure your data contains valid entries.")

        gb = GradientBoostingRegressor(max_depth=4, n_estimators=100, random_state=2)
        gb.fit(X, Y)

        model_dir = 'allmodels'
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        model_path = os.path.join(model_dir, f'{model_name}.pkl')
        joblib.dump(gb, model_path)

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
# retrain_model('PTL')
