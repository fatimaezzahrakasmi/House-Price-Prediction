import pickle
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Load the saved model and scaler
try:
    loaded_model = pickle.load(open('../models/model.sav', 'rb'))
    scaler = pickle.load(open('../models/scaler.sav', 'rb'))
    print("Model and scaler loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading model or scaler: {e}")
    print("Please make sure 'model.sav' and 'scaler.sav' are in the same directory.")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract features in the correct order:
        # bedrooms, bathrooms, floors, grade, yr_built, zipcode
        features = [
            data.get('bedrooms', 0),
            data.get('bathrooms', 0),
            data.get('floors', 0),
            data.get('grade', 0),
            data.get('yr_built', 0),
            data.get('zipcode', 0)
        ]
        
        # Convert to numpy array and reshape
        input_data = np.array(features).reshape(1, -1)
        
        # Scale the data using the saved scaler
        input_data_scaled = scaler.transform(input_data)

        # Make predictions using the loaded model
        price_prediction = loaded_model.predict(input_data_scaled)[0]

        response = {
            'predicted_price': float(price_prediction),
            'status': 'success'
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
