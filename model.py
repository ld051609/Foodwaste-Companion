import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDRegressor, LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import csv
from sklearn.preprocessing import StandardScaler

dataset = './FAO-dataset.csv'
df = pd.read_csv(dataset)

def get_country_production_prediction_model(df, country):
    filtered_df = df[df['Area'] == country]
    food_items = filtered_df['Item'].unique()
    my_list_dict = []
    for food_item in food_items:
        # Filter the data based on food item
        filtered_df_item = filtered_df[filtered_df['Item'] == food_item]
        
        if filtered_df_item.empty:
            print(f"No data available for {food_item} in {country}. Skipping.")
            continue
                
        # Prepare data for model
        X = filtered_df_item[['Year']].values
        y = filtered_df_item['Value'].values

        # Initialize scaler
        scaler = StandardScaler()

        # Fit and transform X_train
        X_train_scaled = scaler.fit_transform(X)

        # Initialize and train SGDRegressor with scaled data
        model = SGDRegressor(random_state=42)
        model.fit(X_train_scaled, y)

        # Make predictions for a future year (e.g., 2025)
        future_year = 2025
        predictions_scaled = model.predict(scaler.transform([[future_year]]))
        # print(f"Predicted value for {country} in {future_year} of {food_item}: {predictions_scaled[0]}")

        my_list_dict.append({'Item': food_item, f'Production prediction in {future_year}': predictions_scaled[0]})
    
    # Sort the list of dictionaries by the predicted production value in the future year in descending order
    sorted_list_dict = sorted(my_list_dict, key=lambda x: x[f'Production prediction in {future_year}'], reverse=True)

    # Return the top 5 food items with the highest predicted production value in the future year
    return sorted_list_dict[:5]

# Example usage
list = get_country_production_prediction_model(df, 'Afghanistan')





