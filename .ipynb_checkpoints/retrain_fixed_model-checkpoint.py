import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import json

def fix_notebook():
    try:
        with open('HousesPricesPrediction.ipynb', 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # We will iterate over cells and comment out the lines that apply 
        # replace_outliers_with_median so the user's notebook is fixed.
        for cell in nb.get('cells', []):
            if cell.get('cell_type') == 'code':
                new_source = []
                for line in cell.get('source', []):
                    # Comment out the call to the function that ruins the data
                    if 'new_df = replace_outliers_with_median(new_df, col)' in line:
                        new_source.append('# ' + line + '  # [FIXED] Removed mathematically incorrect outlier replacement\n')
                    else:
                        new_source.append(line)
                cell['source'] = new_source
                
        with open('HousesPricesPrediction.ipynb', 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print("Notebook 'HousesPricesPrediction.ipynb' fixed successfully.")
    except Exception as e:
        print(f"Error fixing notebook: {e}")

def retrain_models():
    print("Loading data...")
    data = pd.read_csv('data/kc_house_data.csv')
    
    selected_features = ['bedrooms', 'bathrooms', 'floors', 'grade', 'yr_built', 'zipcode']
    X = data[selected_features]
    y = data['price']
    
    print("Splitting and scaling data (without median outlier replacement!)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Training Tuned MLPRegressor...")
    mlp_model_tuned = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, learning_rate_init=0.001, random_state=42)
    mlp_model_tuned.fit(X_train_scaled, y_train)
    
    y_pred_mlp_tuned = mlp_model_tuned.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred_mlp_tuned)
    r2 = r2_score(y_test, y_pred_mlp_tuned)
    
    print("\nMulti-layer Perceptron (Tuned Hyperparameters) [FIXED]:")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    
    # Save the best model and scaler
    print("Saving updated model and scaler...")
    pickle.dump(mlp_model_tuned, open("models/model.sav", "wb"))
    pickle.dump(scaler, open("models/scaler.sav", "wb"))
    pickle.dump(r2, open("models/r2.sav", "wb"))
    print("Models saved successfully in 'models/' directory.")

if __name__ == '__main__':
    fix_notebook()
    retrain_models()
