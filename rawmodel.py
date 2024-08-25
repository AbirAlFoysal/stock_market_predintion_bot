import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

# fix_yahoo_finance is used to fetch data 
import yfinance as yf
# yf.pdr_override()


csv_file_path = r"D:\AbleAid\StockPradiction\DB_csv\unadjusted_amarstock\1JANATAMF.csv"

# Load the CSV file into a DataFrame
dataset = pd.read_csv(csv_file_path)


# Example: Fetching data for Apple Inc. (AAPL)
# dataset = yf.download("AMD", start="2007-01-01", end="2018-11-16")
print(dataset.head())


# View Columns
dataset.head()


dataset['Increase_Decrease'] = np.where(dataset['volume'].shift(-1) > dataset['volume'],1,0)
dataset['Buy_Sell_on_Open'] = np.where(dataset['opening'].shift(-1) > dataset['opening'],1,0)
dataset['Buy_Sell'] = np.where(dataset['adj_close'].shift(-1) > dataset['adj_close'],1,0)
dataset['Returns'] = dataset['adj_close'].pct_change()
dataset = dataset.dropna()
dataset.head()

X = dataset[['opening', 'high', 'low', 'volume']].values
Y = dataset['adj_close'].values


# from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 1/4, random_state = 0) 

print("train length: " , len(X_train))
print("test length: " , len(X_test))

# Checking the minimum, maximum, and average values of Y_test
min_value = Y_test.min()
max_value = Y_test.max()
average_value = Y_test.mean()

print("Minimum value of Y_test: {:.3f}".format(min_value))
print("Maximum value of Y_test: {:.3f}".format(max_value))
print("Average value of Y_test: {:.3f}".format(average_value))

from sklearn.ensemble import GradientBoostingRegressor

gb = GradientBoostingRegressor(max_depth=4, 
            n_estimators=200,
            random_state=2)

# Fit gb to the training set
gb.fit(X_train, Y_train)

# Predict test set labels
y_pred = gb.predict(X_test)

import joblib
joblib.dump(gb, 'gradient_boosting_model.pkl')

from sklearn.metrics import mean_squared_error as MSE

# Compute MSE
mse_test = MSE(Y_test, y_pred)

# Compute RMSE
rmse_test = mse_test**(1/2)

# Print RMSE
print('Test set RMSE of gb: {:.3f}'.format(rmse_test))