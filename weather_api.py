from flask import Flask, jsonify, render_template
from sensor_read import read_dht11, read_mq135
from ai_detection  import detect_anomaly
app = Flask(__name__)
@app.route("/")      ;   def index(): return render_template("dashboard.html")
@app.route("/data")  ;   def data():
    t,h = read_dht11(); g = read_mq135()
    return jsonify({"temperature":t,"humidity":h,"gas":g,
                    "anomaly": detect_anomaly(t,g)})
if __name__=="__main__": app.run(host="0.0.0.0",port=8080)
