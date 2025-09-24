from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)  # Allow React frontend to communicate

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "random_forest_model.joblib")
csv_path = os.path.join(BASE_DIR, "../csv-files/clean_data.csv")

# Load model
model_data = joblib.load(model_path)

# Load CSV
df = pd.read_csv(csv_path)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        location = data.get("location")
        cuisine = data.get("cuisine")
        price = data.get("price", 0)

        if not location or not cuisine:
            return jsonify({"error": "Missing location or cuisine"}), 400

        # Filter dataframe
        df_location = df[df['Location'].str.contains(location, case=False)]
        if df_location.empty:
            return jsonify({"error": "No data for this location"}), 404

        popular_cuisine = df_location['Cuisines'].mode()[0]
        average_price = df_location['Price_for_one'].mean()

        most_popular_restaurant = df_location.loc[df_location['Rating'].idxmax()]
        most_popular_restaurant_name = most_popular_restaurant['Name']

        cuisine_filter = df_location['Cuisines'].str.contains(cuisine, case=False)
        if not df_location[cuisine_filter].empty:
            most_popular_cuisine_restaurant = df_location[cuisine_filter].loc[df_location[cuisine_filter]['Rating'].idxmax()]
            most_popular_cuisine_restaurant_name = most_popular_cuisine_restaurant['Name']
        else:
            most_popular_cuisine_restaurant_name = "Not Found"

        # Prepare input for model
        input_df = pd.DataFrame({'Location':[location], 'Cuisines':[cuisine]})
        input_df_encoded = pd.get_dummies(input_df).reindex(columns=model_data['train_inputs'].columns, fill_value=0)

        predicted_price = model_data['model'].predict(input_df_encoded)[0]

        suggested_price = predicted_price if price >= predicted_price else min(price * 1.1, predicted_price)

        response = {
            "average_price": average_price,
            "popular_cuisine": popular_cuisine,
            "Popular_Restaurant": most_popular_restaurant_name,
            "Popular_Restaurant_serving_cuisine": most_popular_cuisine_restaurant_name,
            "suggested_price": round(suggested_price, 2)
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/options', methods=['GET'])
def get_options():
    # Extract unique non-empty locations and cuisines from your CSV
    locations = sorted(df['Location'].dropna().unique().tolist())
    cuisines = sorted(df['Cuisines'].dropna().unique().tolist())
    return jsonify({"locations": locations, "cuisines": cuisines})

if __name__ == "__main__":
    app.run(debug=True)
