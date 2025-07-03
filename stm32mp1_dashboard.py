#!/usr/bin/env python3
import gi, random, threading, time
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class Dashboard(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="STM32MP1 Sci-Fi Monitor")
        self.set_default_size(480, 320)
        self.fullscreen()
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))

        grid = Gtk.Grid(column_spacing=20, row_spacing=20, margin=30)
        self.add(grid)

        self.temp = Gtk.Label(label="TEMP: -- °C")
        self.hum  = Gtk.Label(label="HUMIDITY: -- %")
        self.gas  = Gtk.Label(label="GAS: -- ppm")
        self.status = Gtk.Label(label="STATUS: Waiting...")

        for label in [self.temp, self.hum, self.gas, self.status]:
            label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 1))
            label.set_name("label")
            label.set_xalign(0)
            label.set_margin_bottom(10)
            grid.attach(label, 0, grid.get_children().__len__(), 1, 1)

        # Exit button
        btn = Gtk.Button(label="Exit")
        btn.connect("clicked", Gtk.main_quit)
        grid.attach(btn, 0, 4, 1, 1)

        threading.Thread(target=self.update_loop, daemon=True).start()

    def update_loop(self):
        while True:
            t = random.randint(25, 40)
            h = random.randint(40, 80)
            g = random.randint(300, 1200)
            a = t > 35 or g > 1000

            GLib.idle_add(self.temp.set_text, f"TEMP: {t} °C")
            GLib.idle_add(self.hum.set_text,  f"HUMIDITY: {h} %")
            GLib.idle_add(self.gas.set_text,  f"GAS: {g} ppm")
            GLib.idle_add(self.status.set_text,
                          "⚠ ANOMALY DETECTED!" if a else "✔ NORMAL")
            GLib.idle_add(self.status.override_color, Gtk.StateFlags.NORMAL,
                          Gdk.RGBA(1, 0, 0, 1) if a else Gdk.RGBA(0, 1, 0, 1))
            time.sleep(2)

if __name__ == "__main__":
    win = Dashboard()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
