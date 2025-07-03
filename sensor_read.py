import time
import os

def read_dht11():
    try:
        os.system("echo 225 > /sys/class/gpio/export")
        os.system("echo in > /sys/class/gpio/gpio225/direction")
        value = os.popen("cat /sys/class/gpio/gpio225/value").read().strip()
        return int(value), 50  # simulate 50% humidity
    except:
        return 0, 0

def read_mq135():
    try:
        with open("/sys/bus/iio/devices/iio:device1/in_voltage14_raw") as f:
            return int(f.read().strip())
    except:
        return 0
