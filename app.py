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
                "Hawa bilkul saaf hai! Outdoor activities ke liye perfect din hai.")
    elif aqi <= 100:
        return ("Satisfactory", "yellow",
                "Hawa theek hai. Sensitive logon ko thoda dhyan rakhna chahiye.")
    elif aqi <= 200:
        return ("Moderate", "orange",
                "Sensitive groups — heart ya lung patients — bahar kam niklen.")
    elif aqi <= 300:
        return ("Poor", "red",
                "Sabko breathing problem ho sakti hai. Mask pehnna recommended hai.")
    elif aqi <= 400:
        return ("Very Poor", "purple",
                "Bahut kharab hawa! Bahar nikalna avoid karo, windows band rakho.")
    else:
        return ("Severe", "maroon",
                "Emergency level pollution! Ghar se bilkul mat nikalna. N95 must.")

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
                message=message
            )
        except Exception as e:
            return render_template('predict.html',
                                   error=f"Sahi number daal bhai! ({str(e)})",
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
