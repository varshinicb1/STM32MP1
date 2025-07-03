def detect_anomaly(temp, gas):
    # Simple rule-based logic: adjust thresholds as needed
    return temp > 35 or gas > 1000
