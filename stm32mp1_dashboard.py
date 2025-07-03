#!/usr/bin/env python3
import os
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread

# === Sensor Functions ===
def read_dht11():
    try:
        os.system("echo 225 > /sys/class/gpio/export")
        os.system("echo in > /sys/class/gpio/gpio225/direction")
        value = os.popen("cat /sys/class/gpio/gpio225/value").read().strip()
        temperature = int(value) * 10  # Simulated conversion
        humidity = 55  # Simulated value
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

# === GUI Code ===
class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STM32MP1 ENV Dashboard")
        self.root.geometry("480x320")
        self.root.configure(bg='black')

        self.temp_var = tk.StringVar()
        self.hum_var = tk.StringVar()
        self.gas_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self.build_ui()
        self.update_data()

    def build_ui(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TLabel", background='black', foreground='cyan', font=('Consolas', 16))
        style.configure("Data.TLabel", foreground='white', font=('Consolas', 20, 'bold'))
        style.configure("Status.TLabel", font=('Consolas', 18, 'bold'))

        frame = ttk.Frame(self.root, padding=10, style="TFrame")
        frame.pack(expand=True)

        # Labels
        for label, var in [("TEMP (°C)", self.temp_var), ("HUMIDITY (%)", self.hum_var), ("GAS", self.gas_var)]:
            ttk.Label(frame, text=label).pack(anchor='w')
            ttk.Label(frame, textvariable=var, style="Data.TLabel").pack(anchor='center', pady=2)

        # Status
        ttk.Label(frame, text="STATUS").pack(anchor='w', pady=(10, 0))
        self.status_label = ttk.Label(frame, textvariable=self.status_var, style="Status.TLabel")
        self.status_label.pack(anchor='center', pady=5)

        # Refresh Button
        ttk.Button(self.root, text="🔄 Refresh", command=self.update_data).pack(side='bottom', pady=8)

    def update_data(self):
        temp, hum = read_dht11()
        gas = read_mq135()
        anomaly = detect_anomaly(temp, gas)

        self.temp_var.set(f"{temp}")
        self.hum_var.set(f"{hum}")
        self.gas_var.set(f"{gas}")

        if anomaly:
            self.status_var.set("⚠ Anomaly Detected!")
            self.status_label.configure(foreground='red')
        else:
            self.status_var.set("✔ Normal")
            self.status_label.configure(foreground='lime')

        self.root.after(3000, self.update_data)

# === Main Execution ===
if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
