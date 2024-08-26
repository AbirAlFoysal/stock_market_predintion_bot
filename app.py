from flask import Flask, render_template, request, jsonify
import pandas as pd
from predict import load_model_and_predict
import json

app = Flask(__name__)

# Load the inquiry.csv file
df_inquiry = pd.read_csv('inquiry.csv')

@app.route('/')
def index():
    shares = df_inquiry['share'].tolist()
    days_options = [7, 30, 60, 90]
    return render_template('index.html', shares=shares, days_options=days_options)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        sample_file = request.form['share']
        days = int(request.form['days'])

        # Call the prediction function
        predictions_json = load_model_and_predict(sample_file, days)

        # Convert JSON string to Python dictionary
        predictions_dict = json.loads(predictions_json)

        # Extract dates and values
        dates = list(predictions_dict.keys())
        values = list(predictions_dict.values())

        # Return a JSON response with dates and values
        return jsonify({'dates': dates, 'values': values})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
