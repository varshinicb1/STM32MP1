import tkinter as tk
from tkinter import font
import threading, time
from sensor_read import get_sensor_data
from ai_detection import detect_anomaly
from logger import log_to_csv

APP_TITLE = "IoT-Based Environmental Monitoring System: Design, Implementation, and Innovation"
AUTHORS = "By: Varshini CB (1RV23EE056), Vedant (1RV23EE057)"

class SciFiDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.configure(bg="#0f2027")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())
        self.current_page = "dashboard"
        self.create_fonts()
        self.create_widgets()
        self.update_data()
        threading.Thread(target=self.periodic_update, daemon=True).start()

    def create_fonts(self):
        self.title_font = font.Font(family="Courier", size=20, weight="bold")
        self.value_font = font.Font(family="Courier", size=16, weight="bold")
        self.label_font = font.Font(family="Courier", size=12)

    def create_widgets(self):
        self.frames = {}
        for page in ("dashboard", "sensors", "about"):
            frame = tk.Frame(self, bg="#0f2027")
            self.frames[page] = frame
            frame.place(relwidth=1, relheight=1)
        self.show_dashboard()
        self.show_page("dashboard")

    def show_dashboard(self):
        f = self.frames["dashboard"]
        for widget in f.winfo_children(): widget.destroy()
        tk.Label(f, text=APP_TITLE, fg="#00ffe7", bg="#0f2027", font=self.title_font).pack(pady=10)
        self.temp_var = tk.StringVar(value="Temperature: -- °C")
        self.hum_var = tk.StringVar(value="Humidity: -- %")
        self.gas_var = tk.StringVar(value="Gas Level: --")
        self.status_var = tk.StringVar(value="Status: --")
        self.source_var = tk.StringVar(value="Source: --")
        for var in [self.temp_var, self.hum_var, self.gas_var, self.status_var, self.source_var]:
            tk.Label(f, textvariable=var, fg="#fff", bg="#0f2027", font=self.value_font).pack(pady=5)
        tk.Button(f, text="Sensors Page", command=lambda: self.show_page("sensors"),
                  fg="#00ffe7", bg="#222", font=self.label_font).pack(pady=10)
        tk.Button(f, text="About", command=lambda: self.show_page("about"),
                  fg="#00ffe7", bg="#222", font=self.label_font).pack(pady=5)

    def show_sensors(self):
        f = self.frames["sensors"]
        for widget in f.winfo_children(): widget.destroy()
        tk.Label(f, text="Real-Time Sensor Data", fg="#00ffe7", bg="#0f2027", font=self.title_font).pack(pady=10)
        self.s_temp = tk.StringVar(value="Temperature: -- °C")
        self.s_hum = tk.StringVar(value="Humidity: -- %")
        self.s_gas = tk.StringVar(value="Gas: --")
        for var in [self.s_temp, self.s_hum, self.s_gas]:
            tk.Label(f, textvariable=var, fg="#fff", bg="#0f2027", font=self.value_font).pack(pady=5)
        tk.Button(f, text="Back to Dashboard", command=lambda: self.show_page("dashboard"),
                  fg="#00ffe7", bg="#222", font=self.label_font).pack(pady=10)

    def show_about(self):
        f = self.frames["about"]
        for widget in f.winfo_children(): widget.destroy()
        tk.Label(f, text=APP_TITLE, fg="#00ffe7", bg="#0f2027", font=self.title_font).pack(pady=10)
        tk.Label(f, text=AUTHORS, fg="#fff", bg="#0f2027", font=self.value_font).pack(pady=5)
        tk.Label(f, text="Dynamic Anomaly Detection using AI with Adaptive Sensing and Localized Alerts.\n\nThis dashboard is interactive, full-screen, and robust to sensor/API failures.",
                 fg="#fff", bg="#0f2027", font=self.label_font, wraplength=600, justify="center").pack(pady=10)
        tk.Button(f, text="Back to Dashboard", command=lambda: self.show_page("dashboard"),
                  fg="#00ffe7", bg="#222", font=self.label_font).pack(pady=10)

    def show_page(self, page):
        for p, f in self.frames.items():
            f.place_forget()
        if page == "dashboard":
            self.show_dashboard()
        elif page == "sensors":
            self.show_sensors()
        elif page == "about":
            self.show_about()
        self.frames[page].place(relwidth=1, relheight=1)
        self.current_page = page

    def update_data(self):
        temp, hum, gas, is_mock, source = get_sensor_data()
        anomaly = detect_anomaly(temp, gas)
        log_to_csv(temp, hum, gas, anomaly, source)
        self.temp_var.set(f"Temperature: {temp:.6f} °C")
        self.hum_var.set(f"Humidity: {hum:.6f} %")
        self.gas_var.set(f"Gas Level: {gas:.6f}")
        self.source_var.set(f"Source: {source}")
        self.status_var.set("⚠ Anomaly Detected!" if anomaly else "Normal")
        if self.current_page == "sensors":
            self.s_temp.set(f"Temperature: {temp:.6f} °C")
            self.s_hum.set(f"Humidity: {hum:.6f} %")
            self.s_gas.set(f"Gas: {gas:.6f}")

    def periodic_update(self):
        while True:
            self.after(0, self.update_data)
            time.sleep(2)

if __name__ == "__main__":
    SciFiDashboard().mainloop()
