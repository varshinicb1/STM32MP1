import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
import threading
import time
from sensor_read import get_sensor_data
from ai_detection import detect_anomaly
from adafruit_io_push import push_to_adafruit
from logger import log_to_csv

class SciFiDashboard(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="STM32MP1 Sci-Fi Dashboard")
        self.set_default_size(480, 320)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.07, 0.13, 0.2, 1))
        self.set_border_width(20)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vbox)

        self.title = Gtk.Label(label="🛰️  ENVIRONMENTAL STATUS")
        self.title.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 1))
        self.title.set_name("sci-fi-title")
        vbox.pack_start(self.title, False, False, 0)

        self.temp_label = Gtk.Label(label="Temperature: -- °C")
        self.hum_label = Gtk.Label(label="Humidity: -- %")
        self.gas_label = Gtk.Label(label="Gas Level: --")
        self.source_label = Gtk.Label(label="Source: --")
        self.status_label = Gtk.Label(label="Status: --")
        for lbl in [self.temp_label, self.hum_label, self.gas_label, self.source_label, self.status_label]:
            lbl.set_name("sci-fi-value")
            vbox.pack_start(lbl, False, False, 0)

        self.footer = Gtk.Label(label="Varshini CB – 1RV23EE056 | Vedant – 1RV23EE057 | Bangalore, India")
        self.footer.set_name("sci-fi-footer")
        vbox.pack_end(self.footer, False, False, 0)

        self.apply_css()
        self.update_data()
        self.start_periodic_update()

    def apply_css(self):
        css = b"""
        #sci-fi-title {
            font-size: 28px;
            color: #00ffe7;
            text-shadow: 0 0 10px #00ffe7, 0 0 20px #00ffe7;
            letter-spacing: 2px;
        }
        #sci-fi-value {
            font-size: 22px;
            color: #fff;
            font-family: 'Orbitron', monospace;
            margin: 8px;
        }
        #sci-fi-footer {
            font-size: 14px;
            color: #00ffe7;
            opacity: 0.8;
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def update_data(self):
        temp, hum, gas, is_mock, source = get_sensor_data()
        anomaly = detect_anomaly(temp, gas)
        log_to_csv(temp, hum, gas, anomaly, source)
        try:
            push_to_adafruit(temp, hum, gas, anomaly)
        except Exception as e:
            print(f"Adafruit IO error: {e}")

        self.temp_label.set_text(f"Temperature: {temp:.6f} °C")
        self.hum_label.set_text(f"Humidity: {hum:.6f} %")
        self.gas_label.set_text(f"Gas Level: {gas:.6f}")
        self.source_label.set_text(f"Source: {'STM32MP1 Sensors' if source == 'sensor' else ('Bangalore Weather API' if source == 'weather_api' else 'Mock Data')}")
        if anomaly:
            self.status_label.set_markup('<span foreground="#ff1744" weight="bold">⚠ Anomaly Detected!</span>')
        else:
            self.status_label.set_markup('<span foreground="#00ff6a" weight="bold">Normal</span>')

    def periodic_update(self):
        while True:
            GLib.idle_add(self.update_data)
            time.sleep(2)

    def start_periodic_update(self):
        t = threading.Thread(target=self.periodic_update, daemon=True)
        t.start()

if __name__ == "__main__":
    win = SciFiDashboard()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
