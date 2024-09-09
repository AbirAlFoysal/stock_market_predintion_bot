import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error as MSE
import joblib

# Load the dataset
dataset = pd.read_csv(r'D:\AbleAid\stock_market_predintion_bot\DB_csv\unadjusted_amarstock\1JANATAMF.csv')

# Feature engineering
dataset['Increase_Decrease'] = np.where(dataset['volume'].shift(-1) > dataset['volume'], 1, 0)
dataset['Buy_Sell_on_Open'] = np.where(dataset['opening'].shift(-1) > dataset['opening'], 1, 0)
dataset['Buy_Sell'] = np.where(dataset['adj_close'].shift(-1) > dataset['adj_close'], 1, 0)
dataset['Returns'] = dataset['adj_close'].pct_change()
dataset = dataset.dropna()

# Splitting the data
X = dataset[['opening', 'high', 'low', 'volume']].values
Y = dataset['adj_close'].values
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=1/4, random_state=0)

# Initialize and train the model with fewer epochs
gb = GradientBoostingRegressor(max_depth=4, n_estimators=50, random_state=2)
gb.fit(X_train, Y_train)

# Save the model
joblib.dump(gb, 'testmodels/model.pkl')

# Compute and print RMSE
y_pred = gb.predict(X_test)
mse_test = MSE(Y_test, y_pred)
rmse_test = mse_test**(1/2)
print(f'Test set RMSE of gb: {rmse_test:.3f}')
