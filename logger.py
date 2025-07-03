import csv
from datetime import datetime

def log_to_csv(temp, hum, gas, anomaly, filename="history.csv"):
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now(), temp, hum, gas, anomaly])
