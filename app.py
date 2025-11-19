from flask import Flask, render_template, request
import pandas as pd   # <-- CSV ko load karne ke liye

app = Flask(__name__)

print("AQI Project start ho raha hai...")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

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
                cat, col, msg = "Good", "good", "Hawa saaf hai bhai!"
            elif aqi <= 100:
                cat, col, msg = "Moderate", "moderate", "Thoda dhyan rakhna"
            elif aqi <= 150:
                cat, col, msg = "Unhealthy for Sensitive", "unhealthy-sensitive", "Sensitive log bahar mat niklo"
            elif aqi <= 200:
                cat, col, msg = "Unhealthy", "unhealthy", "Sabko problem ho sakti hai"
            elif aqi <= 300:
                cat, col, msg = "Very Unhealthy", "very-unhealthy", "Bahut kharab hai!"
            else:
                cat, col, msg = "Hazardous", "hazardous", "Ghar se mat nikalna!"

            return render_template(
                'predict.html',
                show=True,
                aqi=round(aqi,1),
                category=cat,
                color=col,
                message=msg
            )
        except:
            return render_template('predict.html', error="Number hi daal bhai!")

    return render_template('predict.html', show=False)

# =============================
# NEW UPDATED DATASETS ROUTE
# =============================
@app.route('/datasets')
def datasets():
    # 👇👇 Yaha apne dataset ka exact file name lagana
    df = pd.read_csv("cleaned_pollution_data.csv")

    # DataFrame ko HTML table me convert karo
    table_html = df.to_html(classes='table table-dark table-striped', index=False)

    return render_template('datasets.html', table=table_html)


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    print("AQI Shield LIVE → http://127.0.0.1:5000")
    app.run(debug=True)
