from flask import Flask, jsonify, render_template
from sensor_read import get_sensor_data
from ai_detection import detect_anomaly
from adafruit_io_push import push_to_adafruit
from logger import log_to_csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/data")
def data():
    temp, hum, gas, is_mock, source = get_sensor_data()
    anomaly = detect_anomaly(temp, gas)
    log_to_csv(temp, hum, gas, anomaly, source)
    push_to_adafruit(temp, hum, gas, anomaly)
    return jsonify({
        "temperature": temp,
        "humidity": hum,
        "gas": gas,
        "anomaly": anomaly,
        "source": source,
        "is_mock": is_mock
    })

@app.route("/about")
def about():
    return jsonify({
        "title": "IoT-Based Environmental Monitoring System",
        "authors": ["Varshini CB – 1RV23EE056", "Vedant – 1RV23EE057"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
