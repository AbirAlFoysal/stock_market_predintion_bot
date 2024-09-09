from flask import Flask, render_template, request, jsonify
import pandas as pd
from predict import load_model_and_predict
import json

app = Flask(__name__)

df_inquiry = pd.read_csv('inquiry.csv')

@app.route('/')
def index():
    shares = df_inquiry['share'].tolist()
    days_options = [1, 2, 3, 4, 5, 6, 7]
    return render_template('index.html', shares=shares, days_options=days_options)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        sample_file = request.form['share']
        days = int(request.form['days'])

        predictions_json = load_model_and_predict(sample_file, days)

        predictions_dict = json.loads(predictions_json)
        
        if 'error' in predictions_dict:
            return jsonify({'error': predictions_dict['error']}), 500

        dates = list(predictions_dict.keys())
        values = list(predictions_dict.values())
        return jsonify({'dates': dates, 'values': values})

    except FileNotFoundError as e:
        print(f"File not found: {str(e)}")
        return jsonify({'error': f"File not found: {str(e)}"}), 404
    except json.JSONDecodeError as e:
        print(f"JSON error: {str(e)}")
        return jsonify({'error': f"Error parsing model prediction data: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
