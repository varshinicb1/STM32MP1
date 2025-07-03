import Adafruit_DHT
def read_dht11(pin=225):
    sensor = Adafruit_DHT.DHT11
    h,t = Adafruit_DHT.read_retry(sensor, pin)
    return t or 0, h or 0
def read_mq135():
    try:
        with open("/sys/bus/iio/devices/iio:device1/in_voltage14_raw") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0
