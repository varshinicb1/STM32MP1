# STM32MP1 Native Sci-Fi Dashboard

## Features
- Native GTK sci-fi dashboard (no web browser needed)
- Robust fallback: always shows data (sensor, weather API, or mock)
- Adafruit IO integration with error handling
- CSV logging with data source
- One-command launch: `python3 dashboard_gtk.py`

## How to Run
pip3 install -r requirements.txt
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
python3 dashboard_gtk.py

text
undefined
8. Directory Structure
text
STM32MP1/
├── ai_detection.py
├── adafruit_io_push.py
├── dashboard_gtk.py
├── history.csv               # (auto-created)
├── logger.py
├── README.md
├── requirements.txt
├── sensor_read.py
How to launch:

Install dependencies as shown in the README.

Run:

bash
python3 dashboard_gtk.py
The sci-fi dashboard will appear on your STM32MP1 LCD, always showing live or fallback data, with Adafruit IO and logging enabled.
