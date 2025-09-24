# 🍽️ Zomato-Data-Analytics
![Logo](https://i.ibb.co/ccj0mFMd/download.png)
![Logo](https://i.ibb.co/Jx1dQqY/Screenshot-53.jpg)

## 📋 Project Description
- Project aims to develop a recommendation model and visualize insights for startups who are planning to open remote kitchen by leveraging data scraped from the Zomato.
- The primary goal is to provide competitive insights and suggestions regarding pricing and location for restaurants.
- The recommendation model will analyze the scraped data and generate recommendations for optimal price for one person and locations for opening new remote restaurants or improving existing ones.

## ✨ Key Features
- 🕷️ Web scraping to collect restaurant data from Zomato.
- 📊 Data processing and analysis to identify trends, patterns, and correlations.
- 🤖 Machine learning models for generating pricing and location recommendations.
- 📈 Interactive Power BI dashboard for visualizing insights.
- 🌐 User-friendly recommendation model website.

## 🛠️ Technologies Used
- **🐍 Python and Libraries**
  * Beautiful Soup (for web scraping)
  * Pandas (for data manipulation)
  * Scikit-learn (for machine learning models)
  * Flask (for backend API)
  * Joblib (for model serialization)
- **📊 Visualization Tool**
  * Power BI (for data visualization)
- **💻 Website**
  * ReactJS (for frontend)
  * Material-UI (for UI components)
  * Axios (for API communication)
  * CSS3 (for custom styling)

## 📁 File Structure
```
zomato-analytics/
├── client/
│   ├── public/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js
│   ├── package-lock.json
│   └── package.json
├── csv-files/
│   ├── clean_data.csv
│   ├── restaurants_data.csv
│   └── restaurants_details.csv
├── dashboard/
│   └── Food_Parcel_Project...
├── notebooks/
│   ├── app.py
│   ├── Food_Projection.ipynb
│   └── random_forest_mod...
└── README.md
```

## ⚙️ Installation & Setup
```bash
# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install flask flask-cors pandas scikit-learn joblib
python app.py
```

```bash
# Frontend Setup
cd frontend
npm install @mui/material @emotion/react @emotion/styled axios
npm start
```

## 🚧 Challenges
- **🍜 Handling Cuisine Values**: One of the major challenges was dealing with the diverse cuisine values provided by different restaurants. Each restaurant served a unique combination of cuisines, making it difficult to standardize and categorize them effectively.
- **🔗 Backend Development and Integration**: Creating a backend using Flask and integrating it with a React frontend posed its own set of challenges.
- **🎯 Machine Learning Model for Location Recommendations**: Developing a machine learning model to recommend optimal locations based on given inputs was a complex task. Improving models accuracy proved to be challenging.
- **⚡ Model Performance and Optimization**: Enhancing the model's predictive capabilities for better recommendations was an ongoing challenge that required further exploration.

## 🖥️ Webpage
![Webpage](https://i.ibb.co/m5F64vR5/Screenshot-2025-09-11-022319.png)

## 📊 Dashboard
![Dashboard](https://i.ibb.co/tM5S2K5R/Screenshot-2025-09-11-031159.png)
Dashboard Link - http://bit.ly/4m9xsRC
## 🎯 Conclusion
The project involved the development of machine learning models for predicting restaurant pricing and optimal locations. The performance of these models varied significantly:

### 💰 Price Prediction Model
The model developed for predicting the price for one person at a restaurant achieved an impressive accuracy score of over 90%. This high level of accuracy demonstrates the model's proficiency in analyzing various factors, such as cuisine type, location, and other relevant features, to provide reliable price estimates.

### 📍 Location Recommendation Model
However, predicting suitable locations proved to be a complex task.
