import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from datetime import timedelta

# Load the dataset 
dataset = pd.read_csv(r'D:\AbleAid\stock_market_predintion_bot\DB_csv\unadjusted_amarstock\1JANATAMF.csv')

# Feature engineering
dataset['Increase_Decrease'] = np.where(dataset['volume'].shift(-1) > dataset['volume'], 1, 0)
dataset['Buy_Sell_on_Open'] = np.where(dataset['opening'].shift(-1) > dataset['opening'], 1, 0)
dataset['Buy_Sell'] = np.where(dataset['adj_close'].shift(-1) > dataset['adj_close'], 1, 0)
dataset['Returns'] = dataset['adj_close'].pct_change()
dataset = dataset.dropna()

# Load the model
gb = joblib.load('testmodels/model.pkl')

# Predict the next 7 days
last_data = dataset[['opening', 'high', 'low', 'volume']].values[-1].reshape(1, -4)
predictions = []
for i in range(7):
    pred = gb.predict(last_data)
    predictions.append(pred[0])
    last_data = np.append(last_data[:, 1:], pred).reshape(1, -4)

# Generate dates for the predictions
last_date = pd.to_datetime(dataset['timestamp'].iloc[-1])
prediction_dates = [last_date + timedelta(days=i+1) for i in range(7)]

# Plot the predictions
plt.figure(figsize=(10, 5))
plt.plot(prediction_dates, predictions, marker='o', linestyle='-')
plt.title('Next 7 Days Predictions')
plt.xlabel('Date')
plt.ylabel('Predicted adj_close')
plt.grid(True)
plt.show()
