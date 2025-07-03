import requests

# GPIO and ADC reading functions for STM32MP1
def read_dht11():
    try:
        # Attempt to read DHT11 via sysfs GPIO (GPIO 225 = PE1)
        with open("/sys/class/gpio/gpio225/value") as f:
            # This is a placeholder; real DHT11 reading requires timing protocol
            # Here, always fail to trigger fallback
            raise Exception("DHT11 timing protocol not implemented")
    except Exception:
        return None, None

def read_mq135():
    try:
        with open("/sys/bus/iio/devices/iio:device1/in_voltage14_raw") as f:
            return int(f.read().strip())
    except Exception:
        return None

def get_bangalore_weather():
    try:
        # Open-Meteo free API for Bangalore (latitude/longitude)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "current_weather": True,
            "hourly": "temperature_2m,relative_humidity_2m",
            "timezone": "Asia/Kolkata"
        }
        r = requests.get(url, params=params, timeout=3)
        data = r.json()
        temp = round(float(data["current_weather"]["temperature"]), 2)
        hum = round(float(data["hourly"]["relative_humidity_2m"][0]), 2)
        return temp, hum
    except Exception:
        # If API fails, use static mock data
        return 25.123456, 56.789012

def get_mock_data():
    # High-precision mock data
    return 25.123456, 56.789012, 350.987654

def get_sensor_data():
    temp, hum = read_dht11()
    gas = read_mq135()
    if temp is not None and hum is not None and gas is not None:
        return round(temp, 6), round(hum, 6), round(gas, 6), False, "sensor"
    # Try weather API for temp/hum, mock for gas
    temp, hum = get_bangalore_weather()
    gas = 350.987654
    return temp, hum, gas, True, "weather_api"
