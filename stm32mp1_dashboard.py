#!/usr/bin/env python3
import gi
import threading
import random
import time
from datetime import datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class SensorData:
    def __init__(self):
        self.temp = 30.0
        self.hum = 50.0
        self.gas = 400
        self.history = []

    def update(self):
        self.temp += random.uniform(-0.5, 0.5)
        self.hum += random.uniform(-1, 1)
        self.gas += random.randint(-20, 20)
        self.temp = max(20, min(45, self.temp))
        self.hum = max(30, min(90, self.hum))
        self.gas = max(200, min(1200, self.gas))
        self.history.append((datetime.now(), self.temp, self.hum, self.gas))
        if len(self.history) > 50:
            self.history.pop(0)
        return self.temp, self.hum, self.gas

class WeatherStation(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Innovative Lab Experiment: IoT-Based Environmental Monitoring System")
        self.set_default_size(800, 480)
        self.fullscreen()
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.05, 0.05, 0.05, 1))

        self.sensor = SensorData()

        self.grid = Gtk.Grid(column_spacing=20, row_spacing=20, margin=20)
        self.grid.set_column_homogeneous(True)
        self.add(self.grid)

        self.title = self.make_label("📡 STM32MP1 Environmental Monitoring Dashboard", 24, (0, 1, 1))
        self.grid.attach(self.title, 0, 0, 2, 1)

        # Sensor widgets
        self.temp_btn = self.make_button("🌡 Temperature: -- °C", self.on_temp_click)
        self.hum_btn = self.make_button("💧 Humidity: -- %", self.on_hum_click)
        self.gas_btn = self.make_button("🧪 Gas Level: -- ppm", self.on_gas_click)
        self.status_label = self.make_label("STATUS: Starting...", 20, (1, 1, 0))

        self.grid.attach(self.temp_btn, 0, 1, 2, 1)
        self.grid.attach(self.hum_btn, 0, 2, 2, 1)
        self.grid.attach(self.gas_btn, 0, 3, 2, 1)
        self.grid.attach(self.status_label, 0, 4, 2, 1)

        self.exit_btn = Gtk.Button(label="❌ Exit")
        self.exit_btn.connect("clicked", Gtk.main_quit)
        self.grid.attach(self.exit_btn, 0, 5, 2, 1)

        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def make_label(self, text, size=20, rgb=(1, 1, 1)):
        label = Gtk.Label(label=text)
        label.set_xalign(0)
        label.set_margin_bottom(10)
        label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(*rgb, 1))
        label.set_markup(f"<span font='Monospace {size}'>{text}</span>")
        return label

    def make_button(self, text, callback):
        btn = Gtk.Button(label=text)
        btn.connect("clicked", callback)
        btn.get_style_context().add_class("suggested-action")
        return btn

    def update_loop(self):
        while True:
            temp, hum, gas = self.sensor.update()
            anomaly = temp > 38 or gas > 1000
            GLib.idle_add(self.temp_btn.set_label, f"🌡 Temperature: {temp:.1f} °C")
            GLib.idle_add(self.hum_btn.set_label, f"💧 Humidity: {hum:.1f} %")
            GLib.idle_add(self.gas_btn.set_label, f"🧪 Gas Level: {gas} ppm")
            GLib.idle_add(self.status_label.set_markup,
                          f"<span font='Monospace 20' foreground='{'red' if anomaly else 'lime'}'>"
                          f"{'⚠ Anomaly Detected!' if anomaly else '✔ System Normal'}</span>")
            time.sleep(3)

    def show_history_popup(self, sensor_name):
        win = Gtk.Window(title=f"{sensor_name} History (Last 50)")
        win.set_default_size(400, 300)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        win.add(box)
        for t, temp, hum, gas in reversed(self.sensor.history):
            label = Gtk.Label()
            label.set_xalign(0)
            label.set_margin_bottom(2)
            if sensor_name == "Temperature":
                label.set_text(f"{t.strftime('%H:%M:%S')} - {temp:.1f} °C")
            elif sensor_name == "Humidity":
                label.set_text(f"{t.strftime('%H:%M:%S')} - {hum:.1f} %")
            else:
                label.set_text(f"{t.strftime('%H:%M:%S')} - {gas} ppm")
            box.pack_start(label, False, False, 0)
        win.show_all()

    def on_temp_click(self, button):
        self.show_history_popup("Temperature")

    def on_hum_click(self, button):
        self.show_history_popup("Humidity")

    def on_gas_click(self, button):
        self.show_history_popup("Gas")

if __name__ == "__main__":
    win = WeatherStation()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
