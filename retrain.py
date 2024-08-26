import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor


def retrain_model(sample_file):
    try:
        csv_directory = "./DB_csv/unadjusted_amarstock/"
        model_directory = "allmodels"
        sample_file = str(sample_file) + ".csv"

        # Ensure model directory exists
        if not os.path.exists(model_directory):
            os.makedirs(model_directory)

        # Load the data
        file_path = os.path.join(csv_directory, sample_file)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file '{file_path}' not found.")

        df = pd.read_csv(file_path)

        # Prepare the dataset
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['day_of_year'] = df['timestamp'].dt.dayofyear
        df['year'] = df['timestamp'].dt.year

        # Create lag features
        df['lag1'] = df['adj_close'].shift(1)
        df['lag2'] = df['adj_close'].shift(2)
        df['rolling_mean'] = df['adj_close'].rolling(window=5).mean()
        df['rolling_std'] = df['adj_close'].rolling(window=5).std()

        # Drop rows with NaN values
        df = df.dropna()

        # Feature and target selection
        X = df[['opening', 'high', 'low', 'volume', 'day_of_year', 'year', 'lag1', 'lag2', 'rolling_mean', 'rolling_std']].values
        Y = df['adj_close'].values

        # Split the data into training and testing sets
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Train the model
        gb = GradientBoostingRegressor(max_depth=4, n_estimators=200, random_state=2)
        gb.fit(X_train, Y_train)

        # Define the model file path
        model_file = os.path.join(model_directory, sample_file.replace('.csv', '.pkl'))

        # Check if the model file already exists and delete it if it does
        if os.path.exists(model_file):
            try:
                os.remove(model_file)
                print(f"Existing model {model_file} deleted.")
            except Exception as e:
                raise RuntimeError(f"Error deleting the existing model file: {e}")

        # Save the trained model as a .pkl file
        try:
            with open(model_file, 'wb') as f:
                pickle.dump(gb, f)
            print(f"New model saved to {model_file}")
        except Exception as e:
            raise RuntimeError(f"Error saving the model: {e}")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except pd.errors.EmptyDataError as ede_error:
        print(f"CSV file is empty or malformed: {ede_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
# retrain_model('ACI')
