#!/usr/bin/env python3
import gi
import os
import time
import threading

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

def read_dht11():
    try:
        os.system("echo 225 > /sys/class/gpio/export")
        os.system("echo in > /sys/class/gpio/gpio225/direction")
        value = os.popen("cat /sys/class/gpio/gpio225/value").read().strip()
        temperature = int(value) * 10
        humidity = 55
        return temperature, humidity
    except:
        return 0, 0

def read_mq135():
    try:
        with open("/sys/bus/iio/devices/iio:device1/in_voltage14_raw") as f:
            return int(f.read().strip())
    except:
        return 0

def detect_anomaly(temp, gas):
    return temp > 35 or gas > 1000

class Dashboard(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="STM32MP1 Environment Monitor")
        self.set_default_size(480, 320)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))

        self.grid = Gtk.Grid(column_spacing=10, row_spacing=10, margin=20)
        self.add(self.grid)

        self.label_temp = Gtk.Label(label="TEMP: -- °C")
        self.label_hum = Gtk.Label(label="HUMIDITY: -- %")
        self.label_gas = Gtk.Label(label="GAS: --")
        self.label_status = Gtk.Label(label="STATUS: Waiting...")

        for label in [self.label_temp, self.label_hum, self.label_gas, self.label_status]:
            label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 1))
            label.set_name("data-label")
            label.set_margin_top(10)
            self.grid.attach(label, 0, len(self.grid.get_children()), 1, 1)

        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def update_loop(self):
        while True:
            temp, hum = read_dht11()
            gas = read_mq135()
            anomaly = detect_anomaly(temp, gas)

            GLib.idle_add(self.label_temp.set_text, f"TEMP: {temp} °C")
            GLib.idle_add(self.label_hum.set_text, f"HUMIDITY: {hum} %")
            GLib.idle_add(self.label_gas.set_text, f"GAS: {gas}")
            GLib.idle_add(
                self.label_status.set_text,
                "⚠ ANOMALY DETECTED!" if anomaly else "✔ STATUS: NORMAL"
            )
            time.sleep(3)

if __name__ == "__main__":
    from gi.repository import Gdk
    win = Dashboard()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
