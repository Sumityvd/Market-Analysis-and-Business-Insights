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
try:
    model_data = joblib.load(model_path)
except FileNotFoundError:
    print("Warning: Model file not found. Prediction functionality will be limited.")
    model_data = None

# Load CSV
try:
    df = pd.read_csv(csv_path)
    print(f"Loaded CSV with {len(df)} rows")
    print(f"Columns: {df.columns.tolist()}")
except FileNotFoundError:
    print("Error: CSV file not found!")
    df = pd.DataFrame()

@app.route('/options', methods=['GET'])
def get_options():
    """Get unique locations and cuisines for dropdown menus"""
    try:
        if df.empty:
            return jsonify({"error": "No data available"}), 500
        
        # Extract unique locations (handle different possible column names)
        location_columns = ['Location', 'location', 'LOCATION']
        location_col = None
        for col in location_columns:
            if col in df.columns:
                location_col = col
                break
        
        # Extract unique cuisines (handle different possible column names)
        cuisine_columns = ['Cuisines', 'cuisines', 'CUISINES', 'Cuisine', 'cuisine']
        cuisine_col = None
        for col in cuisine_columns:
            if col in df.columns:
                cuisine_col = col
                break
        
        locations = []
        cuisines = []
        
        if location_col:
            locations = sorted([loc for loc in df[location_col].dropna().unique() if str(loc).strip()])
        
        if cuisine_col:
            # Handle comma-separated cuisines
            all_cuisines = set()
            for cuisine_entry in df[cuisine_col].dropna():
                if pd.isna(cuisine_entry):
                    continue
                # Split by comma and clean up
                for cuisine in str(cuisine_entry).split(','):
                    cleaned = cuisine.strip()
                    if cleaned:
                        all_cuisines.add(cleaned)
            cuisines = sorted(list(all_cuisines))
        
        return jsonify({
            "locations": locations,
            "cuisines": cuisines,
            "total_records": len(df)
        })
    
    except Exception as e:
        print(f"Error in get_options: {str(e)}")
        return jsonify({"error": f"Failed to fetch options: {str(e)}"}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        location = data.get("location")
        cuisine = data.get("cuisine")
        price = data.get("price", 0)
        
        if not location or not cuisine:
            return jsonify({"error": "Missing location or cuisine"}), 400
        
        if df.empty:
            return jsonify({"error": "No data available for predictions"}), 500
        
        # Determine column names (flexible matching)
        location_col = None
        for col in ['Location', 'location', 'LOCATION']:
            if col in df.columns:
                location_col = col
                break
        
        cuisine_col = None
        for col in ['Cuisines', 'cuisines', 'CUISINES', 'Cuisine', 'cuisine']:
            if col in df.columns:
                cuisine_col = col
                break
                
        price_col = None
        for col in ['Price_for_one', 'price_for_one', 'Price', 'price']:
            if col in df.columns:
                price_col = col
                break
                
        rating_col = None
        for col in ['Rating', 'rating', 'RATING']:
            if col in df.columns:
                rating_col = col
                break
                
        name_col = None
        for col in ['Name', 'name', 'NAME', 'Restaurant_Name', 'restaurant_name']:
            if col in df.columns:
                name_col = col
                break
        
        if not all([location_col, cuisine_col, price_col]):
            return jsonify({"error": "Required columns not found in dataset"}), 500
        
        # Filter dataframe by location
        df_location = df[df[location_col].str.contains(location, case=False, na=False)]
        if df_location.empty:
            return jsonify({"error": f"No data found for location: {location}"}), 404
        
        # Calculate statistics
        popular_cuisine = df_location[cuisine_col].mode()
        popular_cuisine = popular_cuisine[0] if not popular_cuisine.empty else "Not Available"
        
        average_price = df_location[price_col].mean()
        
        # Find most popular restaurant (highest rated)
        most_popular_restaurant_name = "Not Available"
        if rating_col and name_col:
            if not df_location[rating_col].isna().all():
                most_popular_restaurant = df_location.loc[df_location[rating_col].idxmax()]
                most_popular_restaurant_name = most_popular_restaurant[name_col]
        
        # Find most popular restaurant serving the specific cuisine
        cuisine_filter = df_location[cuisine_col].str.contains(cuisine, case=False, na=False)
        most_popular_cuisine_restaurant_name = "Not Found"
        
        if not df_location[cuisine_filter].empty and rating_col and name_col:
            cuisine_restaurants = df_location[cuisine_filter]
            if not cuisine_restaurants[rating_col].isna().all():
                most_popular_cuisine_restaurant = cuisine_restaurants.loc[cuisine_restaurants[rating_col].idxmax()]
                most_popular_cuisine_restaurant_name = most_popular_cuisine_restaurant[name_col]
        
        # Model prediction (if model is available)
        suggested_price = price
        if model_data:
            try:
                # Prepare input for model
                input_df = pd.DataFrame({location_col: [location], cuisine_col: [cuisine]})
                input_df_encoded = pd.get_dummies(input_df).reindex(
                    columns=model_data['train_inputs'].columns, 
                    fill_value=0
                )
                predicted_price = model_data['model'].predict(input_df_encoded)[0]
                suggested_price = predicted_price if price >= predicted_price else min(price * 1.1, predicted_price)
            except Exception as model_error:
                print(f"Model prediction error: {model_error}")
                # Fallback to average price
                suggested_price = average_price if average_price else price
        
        response = {
            "average_price": round(average_price, 2) if average_price else 0,
            "popular_cuisine": popular_cuisine,
            "Popular_Restaurant": most_popular_restaurant_name,
            "Popular_Restaurant_serving_cuisine": most_popular_cuisine_restaurant_name,
            "suggested_price": round(suggested_price, 2)
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in predict: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "data_loaded": not df.empty,
        "model_loaded": model_data is not None,
        "records": len(df) if not df.empty else 0
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)