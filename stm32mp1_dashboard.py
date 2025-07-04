#!/usr/bin/env python3
import gi, random, threading, time
from datetime import datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class WeatherStation(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="STM32MP1 Weather Station")
        self.set_default_size(800, 480)
        self.fullscreen()
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.05, 0.05, 0.05, 1))

        self.history = []
        self.grid = Gtk.Grid(column_spacing=20, row_spacing=10, margin_top=10, margin_bottom=10, margin_start=20, margin_end=20)
        self.grid.set_column_homogeneous(True)
        self.add(self.grid)

        # Project Title Info on Display
        title = self.make_label("🛰 IoT-Based Environmental Monitoring System", 20, (0.4, 1.0, 1.0))
        subtitle = self.make_label("🔍 Anomaly Detection with Adaptive Sensing", 16, (0.7, 0.9, 1.0))
        authors = self.make_label("👩‍🔬 Varshini CB (1RV23EE056) | 👨‍🔬 Vedant (1RV23EE057)", 14, (0.8, 0.8, 0.8))

        self.grid.attach(title, 0, 0, 2, 1)
        self.grid.attach(subtitle, 0, 1, 2, 1)
        self.grid.attach(authors, 0, 2, 2, 1)

        # Sensor data widgets
        self.temp = self.make_label("🌡 Temperature: -- °C", 24)
        self.hum = self.make_label("💧 Humidity: -- %", 24)
        self.gas = self.make_label("🧪 Air Quality: Medium", 24)
        self.status = self.make_label("✔ System Status: Initializing...", 24, (1, 1, 0))

        labels = [self.temp, self.hum, self.gas, self.status]
        for i, lbl in enumerate(labels):
            self.grid.attach(lbl, 0, i + 3, 2, 1)

        # Exit button
        exit_btn = Gtk.Button(label="❌ Exit")
        exit_btn.connect("clicked", Gtk.main_quit)
        self.grid.attach(exit_btn, 0, 8, 2, 1)

        # Start data simulation
        self.temp_val = 30.0
        self.hum_val = 50.0
        self.gas_val = 500

        self.updater = threading.Thread(target=self.update_loop)
        self.updater.daemon = True
        self.updater.start()

    def make_label(self, text, size=20, rgb=(1, 1, 1)):
        lbl = Gtk.Label(label=text)
        lbl.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(*rgb, 1))
        lbl.set_xalign(0.0)
        lbl.set_margin_bottom(6)
        lbl.set_markup(f"<span font='Monospace {size}'>{text}</span>")
        return lbl

    def update_loop(self):
        while True:
            self.temp_val += random.uniform(-0.3, 0.3)
            self.hum_val += random.uniform(-0.5, 0.5)
            self.gas_val += random.randint(-10, 10)

            self.temp_val = max(20, min(45, self.temp_val))
            self.hum_val = max(30, min(90, self.hum_val))
            self.gas_val = max(300, min(1000, self.gas_val))

            status = "⚠ ALERT: High Temp/Gas" if self.gas_val > 900 or self.temp_val > 40 else "✔ System Stable"
            air_quality = "Good" if self.gas_val < 400 else "Medium" if self.gas_val < 800 else "Poor"
            self.history.append((datetime.now(), self.temp_val, self.hum_val, self.gas_val))
            if len(self.history) > 50:
                self.history.pop(0)

            # Update GUI
            GLib.idle_add(self.temp.set_markup, f"<span font='Monospace 24'>🌡 Temperature: {self.temp_val:.1f} °C</span>")
            GLib.idle_add(self.hum.set_markup, f"<span font='Monospace 24'>💧 Humidity: {self.hum_val:.1f} %</span>")
            GLib.idle_add(self.gas.set_markup, f"<span font='Monospace 24'>🧪 Air Quality: {air_quality}</span>")
            GLib.idle_add(self.status.set_markup, f"<span font='Monospace 24'>{status}</span>")
            GLib.idle_add(self.status.override_color, Gtk.StateFlags.NORMAL,
                          Gdk.RGBA(1, 0, 0, 1) if "ALERT" in status else Gdk.RGBA(0, 1, 0, 1))
            time.sleep(3)

if __name__ == "__main__":
    win = WeatherStation()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
