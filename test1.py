import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error as MSE, r2_score
from sklearn.model_selection import train_test_split

def predict_future_prices(days=7):
    # Directory containing the CSV files
    csv_directory = r'D:\AbleAid\StockPradiction\DB_csv\unadjusted_amarstock'
    model_directory = r'D:\AbleAid\StockPradiction\models'

    # Ensure model directory exists
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)

    # Select a sample CSV file to train and predict
    sample_file = 'ACI.csv'  # Replace with your actual file
    file_path = os.path.join(csv_directory, sample_file)

    df = pd.read_csv(file_path)

    # Prepare the dataset
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['day_of_year'] = df['timestamp'].dt.dayofyear
    df['year'] = df['timestamp'].dt.year

    # Feature and target selection
    X = df[['opening', 'high', 'low', 'volume', 'day_of_year', 'year']].values
    Y = df['adj_close'].values

    # Split the data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Train the model
    gb = GradientBoostingRegressor(max_depth=4, n_estimators=200, random_state=2)
    gb.fit(X_train, Y_train)

    # Predict and calculate RMSE on test data
    y_pred_test = gb.predict(X_test)
    test_rmse = MSE(Y_test, y_pred_test) ** 0.5
    accuracy = r2_score(Y_test, y_pred_test)

    # Predict the adj_close for the next 'days' days
    last_known_day = df['day_of_year'].iloc[-1]
    last_known_year = df['year'].iloc[-1]

    future_predictions = []
    for day in range(1, days + 1):
        next_day_of_year = (last_known_day + day) % 365
        next_year = last_known_year + (last_known_day + day) // 365

        # Use the last known values of opening, high, low, volume for predictions
        last_row = df.iloc[-1][['opening', 'high', 'low', 'volume']].values
        prediction = gb.predict([np.append(last_row, [next_day_of_year, next_year])])
        future_predictions.append(prediction[0])

    # Print the predicted values
    print(f"Predicted adj_close prices for the next {days} days:")
    for i, prediction in enumerate(future_predictions, start=1):
        print(f"Day {i}: {prediction:.2f}")

    print(f"\nTest RMSE: {test_rmse}")
    print(f"Accuracy (R2 Score): {accuracy * 100:.2f}%")

    return future_predictions

# Example usage:
predictions = predict_future_prices(days=70)
