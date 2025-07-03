<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>STM32MP1 Sci-Fi Dashboard</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="neon-container">
    <h1 class="neon-title">🛰️ STM32MP1 ENVIRONMENTAL DASHBOARD</h1>
    <div class="neon-panel">
      <div class="neon-row">
        <span class="label">Temperature</span>
        <span class="value" id="temp">--</span>
        <span class="unit">°C</span>
      </div>
      <div class="neon-row">
        <span class="label">Humidity</span>
        <span class="value" id="hum">--</span>
        <span class="unit">%</span>
      </div>
      <div class="neon-row">
        <span class="label">Gas Level</span>
        <span class="value" id="gas">--</span>
      </div>
      <div class="neon-row">
        <span class="label">Source</span>
        <span class="value" id="source">--</span>
      </div>
      <div class="neon-row">
        <span class="label">Status</span>
        <span class="value" id="anomaly" class="safe">--</span>
      </div>
    </div>
    <footer>
      <span>Varshini CB – 1RV23EE056 | Vedant – 1RV23EE057</span>
      <span class="footer-right">Bangalore, India</span>
    </footer>
  </div>
<script>
function update() {
  fetch("/data").then(r => r.json()).then(d => {
    document.getElementById("temp").innerText = d.temperature.toFixed(6);
    document.getElementById("hum").innerText  = d.humidity.toFixed(6);
    document.getElementById("gas").innerText  = d.gas.toFixed(6);
    document.getElementById("source").innerText = d.source === "sensor" ? "STM32MP1 Sensors" : (d.source === "weather_api" ? "Bangalore Weather API" : "Mock Data");
    let anomalyElem = document.getElementById("anomaly");
    if (d.anomaly) {
      anomalyElem.innerText = "⚠ Anomaly Detected!";
      anomalyElem.className = "alert";
    } else {
      anomalyElem.innerText = "Normal";
      anomalyElem.className = "safe";
    }
  }).catch(() => {
    // UI never fails: show placeholder
    document.getElementById("temp").innerText = "25.123456";
    document.getElementById("hum").innerText  = "56.789012";
    document.getElementById("gas").innerText  = "350.987654";
    document.getElementById("source").innerText = "Mock Data";
    let anomalyElem = document.getElementById("anomaly");
    anomalyElem.innerText = "Normal";
    anomalyElem.className = "safe";
  });
}
setInterval(update, 2000); update();
</script>
</body>
</html>
