#!/usr/bin/env python3
import gi
import os
import time
import random
import threading

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

# Set full brightness
def set_brightness_max():
    try:
        path = "/sys/class/backlight/backlight"
        with open(f"{path}/max_brightness") as f:
            max_val = f.read().strip()
        with open(f"{path}/brightness", "w") as f:
            f.write(max_val)
    except:
        pass

# Simulated sensor functions
def read_dht11():
    return random.randint(25, 40), random.randint(40, 80)

def read_mq135():
    return random.randint(400, 1200)

def detect_anomaly(temp, gas):
    return temp > 35 or gas > 1000

class Dashboard(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="STM32MP1 Dashboard")
        self.set_default_size(800, 480)
        self.fullscreen()
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.05, 0.05, 0.05, 1))

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(20)
        self.grid.set_row_spacing(30)
        self.grid.set_border_width(40)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(False)
        self.add(self.grid)

        # Title
        self.title = self.make_label("🛰 STM32MP1 ENVIRONMENTAL MONITOR", 32, (0, 1, 1))
        self.grid.attach(self.title, 0, 0, 2, 1)

        # Data labels
        self.temp_label = self.make_label("🌡 TEMP: -- °C", 28)
        self.hum_label  = self.make_label("💧 HUMIDITY: -- %", 28)
        self.gas_label  = self.make_label("🧪 GAS: -- ppm", 28)
        self.status_label = self.make_label("STATUS: BOOTING...", 30, (1, 1, 0))

        self.grid.attach(self.temp_label, 0, 1, 2, 1)
        self.grid.attach(self.hum_label, 0, 2, 2, 1)
        self.grid.attach(self.gas_label, 0, 3, 2, 1)
        self.grid.attach(self.status_label, 0, 4, 2, 1)

        # Exit button (optional touch)
        self.exit_button = Gtk.Button(label="❌ Exit")
        self.exit_button.get_style_context().add_class("suggested-action")
        self.exit_button.connect("clicked", Gtk.main_quit)
        self.grid.attach(self.exit_button, 0, 5, 2, 1)

        # Start update thread
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def make_label(self, text, size, rgb=(1, 1, 1)):
        label = Gtk.Label(label=text)
        label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(*rgb, 1))
        label.set_name("big-label")
        label.set_xalign(0.5)
        label.set_margin_bottom(10)
        label.set_margin_top(10)
        label.set_markup(f"<span font='Ubuntu Mono {size}'>{text}</span>")
        return label

    def update_loop(self):
        while True:
            temp, hum = read_dht11()
            gas = read_mq135()
            anomaly = detect_anomaly(temp, gas)

            GLib.idle_add(self.temp_label.set_markup,
                          f"<span font='Ubuntu Mono 28'>🌡 TEMP: {temp} °C</span>")
            GLib.idle_add(self.hum_label.set_markup,
                          f"<span font='Ubuntu Mono 28'>💧 HUMIDITY: {hum} %</span>")
            GLib.idle_add(self.gas_label.set_markup,
                          f"<span font='Ubuntu Mono 28'>🧪 GAS: {gas} ppm</span>")
            if anomaly:
                GLib.idle_add(self.status_label.set_markup,
                              "<span font='Ubuntu Mono 30' foreground='red'>⚠ ANOMALY DETECTED!</span>")
            else:
                GLib.idle_add(self.status_label.set_markup,
                              "<span font='Ubuntu Mono 30' foreground='lime'>✔ NORMAL CONDITIONS</span>")
            time.sleep(2)

if __name__ == "__main__":
    set_brightness_max()
    win = Dashboard()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
