from flask import Flask, jsonify, render_template
from sensor_read import read_dht11, read_mq135
from ai_detection import detect_anomaly
from adafruit_io_push import push_to_adafruit
from logger import log_to_csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/data")
def data():
    temp, hum = read_dht11()
    gas = read_mq135()
    anomaly = detect_anomaly(temp, gas)
    # Log and push data
    log_to_csv(temp, hum, gas, anomaly)
    push_to_adafruit(temp, hum, gas, anomaly)
    return jsonify({
        "temperature": temp,
        "humidity": hum,
        "gas": gas,
        "anomaly": anomaly
    })

@app.route("/about")
def about():
    return jsonify({
        "title": "IoT-Based Environmental Monitoring System",
        "authors": ["Varshini CB – 1RV23EE056", "Vedant – 1RV23EE057"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
