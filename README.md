# House Price Prediction

An end-to-end Machine Learning project to predict house prices based on various features such as bedrooms, bathrooms, floors, grade, year built, and zipcode. The project includes data exploration, model training, and a web-based UI for making predictions.

## Project Structure

- `HousesPricesPrediction.ipynb`: Jupyter notebook containing data analysis, preprocessing, and model training (Linear Regression, SVM, MLP).
- `src/app.py`: Flask API server that loads the trained model and scaler to serve predictions.
- `src/ui.py`: Flet desktop/web frontend that provides a user interface to input house features and displays the predicted price.
- `models/model.sav`, `models/scaler.sav`: Saved weights and scaler for the best performing model.
- `data/kc_house_data.csv`: The dataset used for training the model.

## Setup and Installation

1. **Install Dependencies:**
   Ensure you have Python installed. Install the required packages:
   ```bash
   pip install flask flet scikit-learn numpy pandas
   ```

2. **Run the API Server:**
   Open a terminal and start the Flask backend:
   ```bash
   cd src
   python app.py
   ```
   The API will start running on `http://127.0.0.1:5000`.

3. **Run the UI:**
   Open a **new, separate** terminal and run the Flet frontend:
   ```bash
   cd src
   python ui.py
   ```

## Model Details

- **Best Model:** Multi-Layer Perceptron (Tuned)
- Preprocessing involves standard scaling of numerical features using `StandardScaler`.
- Various models were evaluated using Mean Squared Error (MSE) and R-squared metrics.
