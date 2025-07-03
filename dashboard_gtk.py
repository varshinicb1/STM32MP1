import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
import threading, time

from sensor_read import get_sensor_data
from ai_detection import detect_anomaly
from logger import log_to_csv

APP_TITLE = "IoT-Based Environmental Monitoring System: Design, Implementation, and Innovation"
AUTHORS = "By: Varshini CB (1RV23EE056), Vedant (1RV23EE057)"

class DashboardPage(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_name("sci-fi-bg")
        self.parent = parent

        self.title = Gtk.Label(label=APP_TITLE)
        self.title.set_name("sci-fi-title")
        self.pack_start(self.title, False, False, 0)

        self.temp_label = Gtk.Label(label="Temperature: -- °C")
        self.hum_label = Gtk.Label(label="Humidity: -- %")
        self.gas_label = Gtk.Label(label="Gas Level: --")
        self.status_label = Gtk.Label(label="Status: --")
        self.source_label = Gtk.Label(label="Source: --")
        for lbl in [self.temp_label, self.hum_label, self.gas_label, self.status_label, self.source_label]:
            lbl.set_name("sci-fi-value")
            self.pack_start(lbl, False, False, 0)

        self.switch_btn = Gtk.Button(label="Go to Sensors Page")
        self.switch_btn.connect("clicked", lambda w: parent.show_page("sensors"))
        self.pack_start(self.switch_btn, False, False, 0)

        self.about_btn = Gtk.Button(label="About")
        self.about_btn.connect("clicked", lambda w: parent.show_page("about"))
        self.pack_start(self.about_btn, False, False, 0)

    def update(self, temp, hum, gas, anomaly, source):
        self.temp_label.set_text(f"Temperature: {temp:.6f} °C")
        self.hum_label.set_text(f"Humidity: {hum:.6f} %")
        self.gas_label.set_text(f"Gas Level: {gas:.6f}")
        self.source_label.set_text(f"Source: {source}")
        if anomaly:
            self.status_label.set_markup('<span foreground="#ff1744" weight="bold">⚠ Anomaly Detected!</span>')
        else:
            self.status_label.set_markup('<span foreground="#00ff6a" weight="bold">Normal</span>')

class SensorsPage(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_name("sci-fi-bg")
        self.parent = parent

        self.label = Gtk.Label(label="Real-Time Sensor Data")
        self.label.set_name("sci-fi-title")
        self.pack_start(self.label, False, False, 0)

        self.temp = Gtk.Label(label="Temperature: -- °C")
        self.hum = Gtk.Label(label="Humidity: -- %")
        self.gas = Gtk.Label(label="Gas: --")
        for lbl in [self.temp, self.hum, self.gas]:
            lbl.set_name("sci-fi-value")
            self.pack_start(lbl, False, False, 0)

        self.back_btn = Gtk.Button(label="Back to Dashboard")
        self.back_btn.connect("clicked", lambda w: parent.show_page("dashboard"))
        self.pack_start(self.back_btn, False, False, 0)

    def update(self, temp, hum, gas):
        self.temp.set_text(f"Temperature: {temp:.6f} °C")
        self.hum.set_text(f"Humidity: {hum:.6f} %")
        self.gas.set_text(f"Gas: {gas:.6f}")

class AboutPage(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_name("sci-fi-bg")
        self.parent = parent

        self.title = Gtk.Label(label=APP_TITLE)
        self.title.set_name("sci-fi-title")
        self.pack_start(self.title, False, False, 0)

        self.authors = Gtk.Label(label=AUTHORS)
        self.authors.set_name("sci-fi-value")
        self.pack_start(self.authors, False, False, 0)

        self.desc = Gtk.Label(label="Dynamic Anomaly Detection using AI with Adaptive Sensing and Localized Alerts.\n\nThis dashboard is interactive, full-screen, and robust to sensor/API failures.")
        self.desc.set_line_wrap(True)
        self.desc.set_name("sci-fi-value")
        self.pack_start(self.desc, False, False, 0)

        self.back_btn = Gtk.Button(label="Back to Dashboard")
        self.back_btn.connect("clicked", lambda w: parent.show_page("dashboard"))
        self.pack_start(self.back_btn, False, False, 0)

class SciFiApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=APP_TITLE)
        self.set_default_size(800, 480)
        self.fullscreen()
        self.set_decorated(False)
        self.connect("key-press-event", self.on_key_press)
        self.set_border_width(0)
        self.set_name("sci-fi-bg")

        self.stack = Gtk.Stack()
        self.add(self.stack)

        self.pages = {
            "dashboard": DashboardPage(self),
            "sensors": SensorsPage(self),
            "about": AboutPage(self)
        }
        for name, page in self.pages.items():
            self.stack.add_named(page, name)
        self.show_page("dashboard")
        self.apply_css()
        self.start_periodic_update()

    def show_page(self, name):
        self.stack.set_visible_child_name(name)

    def apply_css(self):
        css = b"""
        #sci-fi-bg {
            background: #0f2027;
        }
        #sci-fi-title {
            font-size: 28px;
            color: #00ffe7;
            letter-spacing: 2px;
        }
        #sci-fi-value {
            font-size: 20px;
            color: #fff;
            font-family: 'Courier', monospace;
            margin: 8px;
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def update_all(self):
        temp, hum, gas, is_mock, source = get_sensor_data()
        anomaly = detect_anomaly(temp, gas)
        log_to_csv(temp, hum, gas, anomaly, source)
        self.pages["dashboard"].update(temp, hum, gas, anomaly, source)
        self.pages["sensors"].update(temp, hum, gas)

    def periodic_update(self):
        while True:
            GLib.idle_add(self.update_all)
            time.sleep(2)

    def start_periodic_update(self):
        t = threading.Thread(target=self.periodic_update, daemon=True)
        t.start()

    def on_key_press(self, widget, event):
        # ESC to exit full screen and close
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()

if __name__ == "__main__":
    win = SciFiApp()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
