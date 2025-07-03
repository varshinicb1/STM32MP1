# STM32MP1 Sci-Fi IoT Dashboard

## Features
- Sci-fi animated, mobile-friendly UI
- Robust fallback: never fails, always shows data
- Uses STM32MP1 sensors, Bangalore weather API, or high-precision mock data
- Adafruit IO integration
- CSV logging with data source
- One-command launch: `python3 weather_api.py`

## How to Run
pip3 install -r requirements.txt
sudo apt-get install libgpiod2
python3 weather_api.py

Visit http://<board-ip>:8080
text
undefined
11. Directory Structure
text
STM32MP1/
├── ai_detection.py
├── adafruit_io_push.py
├── flask-dashboard.service
├── history.csv               # (auto-created)
├── logger.py
├── README.md
├── requirements.txt
├── sensor_read.py
├── static/
│   └── style.css
├── templates/
│   └── dashboard.html
├── weather_api.py
Key Points
UI never fails: If sensors and weather API both fail, mock data is shown with high precision.

Sci-fi look: Neon, animated, and responsive dashboard.

Single command: python3 weather_api.py starts the web UI instantly.

Data source shown: UI displays whether data is from sensors, weather API, or mock.

Adafruit IO and CSV logging: All readings are pushed and logged, regardless of data source.
