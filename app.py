from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            pm25 = float(request.form['PM2_5'])
            pm10 = float(request.form['PM10'])
            no2 = float(request.form['NO2'])
            so2 = float(request.form['SO2'])

            aqi = pm25 * 2.5 + pm10 * 0.8 + no2 * 1.2 + so2 * 1.5

            if aqi <= 50:
                cat, col, msg = "Good", "green", "Hawa saaf hai bhai!"
            elif aqi <= 100:
                cat, col, msg = "Moderate", "yellow", "Thoda dhyan rakhna"
            elif aqi <= 150:
                cat, col, msg = "Unhealthy for Sensitive", "orange", "Sensitive log bahar mat niklo"
            elif aqi <= 200:
                cat, col, msg = "Unhealthy", "red", "Sabko problem ho sakti hai"
            elif aqi <= 300:
                cat, col, msg = "Very Unhealthy", "purple", "Bahut kharab hai!"
            else:
                cat, col, msg = "Hazardous", "maroon", "Ghar se mat nikalna!"

            return render_template(
                'predict.html',
                show=True,
                aqi=round(aqi,1),
                category=cat,
                color=col,
                message=msg
            )

        except:
            return render_template('predict.html', error="Number hi daal bhai!", show=False)

    return render_template('predict.html', show=False)


@app.route('/datasets')
def datasets():
    path = os.path.join(os.path.dirname(__file__), "cleaned_pollution_data.csv")
    df = pd.read_csv(path)
    table_html = df.to_html(classes='table', index=False)
    return render_template('datasets.html', table=table_html)


if __name__ == '__main__':
    app.run(debug=True)
