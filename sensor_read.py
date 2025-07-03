import adafruit_dht
import board

def read_dht11(pin=None):
    # Use board.D4 for GPIO4; adjust as needed for your wiring
    dht_device = adafruit_dht.DHT11(board.D4)
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
    except RuntimeError as error:
        print(error.args[0])
        temperature, humidity = 0, 0
    return temperature or 0, humidity or 0

def read_mq135():
    try:
        with open("/sys/bus/iio/devices/iio:device1/in_voltage14_raw") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0
