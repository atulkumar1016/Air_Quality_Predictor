from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load trained ML model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

def get_category(aqi):
    """Map AQI value to India CPCB category, color class, and message"""
    aqi = round(float(aqi), 1)
    if aqi <= 50:
        return ("Good", "green",
                "Air quality is excellent. No restrictions on outdoor activities.")
    elif aqi <= 100:
        return ("Satisfactory", "yellow",
                "Air quality is acceptable. Unusually sensitive individuals may experience minor discomfort.")
    elif aqi <= 200:
        return ("Moderate", "orange",
                "Sensitive groups — heart or lung disease patients — should limit prolonged outdoor exertion.")
    elif aqi <= 300:
        return ("Poor", "red",
                "Everyone may begin to experience health effects. Wearing a mask outdoors is recommended.")
    elif aqi <= 400:
        return ("Very Poor", "purple",
                "Health alert — serious effects for everyone. Avoid outdoor activities and keep windows closed.")
    else:
        return ("Severe", "maroon",
                "Emergency conditions. Avoid all outdoor exposure. N95 mask is essential if you must go out.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            pm25 = float(request.form['PM2_5'])
            pm10 = float(request.form['PM10'])
            no2  = float(request.form['NO2'])
            so2  = float(request.form['SO2'])

            # Predict using ML model
            features = np.array([[pm25, pm10, no2, so2]])
            aqi_pred = model.predict(features)[0]
            aqi_val  = round(float(aqi_pred), 1)

            category, color, message = get_category(aqi_val)

            return render_template(
                'predict.html',
                show=True,
                aqi=aqi_val,
                category=category,
                color=color,
                message=message,
                aqi_high=(aqi_val > 100)
            )
        except Exception as e:
            return render_template('predict.html',
                                   error=f"Invalid input. Please enter numeric values only. ({str(e)})",
                                   show=False)
    return render_template('predict.html', show=False)

@app.route('/datasets')
def datasets():
    path = os.path.join(os.path.dirname(__file__), 'cleaned_pollution_data.csv')
    df = pd.read_csv(path)
    table_html = df.to_html(classes='data-table', index=False, border=0)
    return render_template('datasets.html', table=table_html)

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
