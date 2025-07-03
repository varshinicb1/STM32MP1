#!/usr/bin/env python3
import os
import pygame
import time

# === Sensor Functions ===
def read_dht11():
    try:
        os.system("echo 225 > /sys/class/gpio/export")
        os.system("echo in > /sys/class/gpio/gpio225/direction")
        value = os.popen("cat /sys/class/gpio/gpio225/value").read().strip()
        temperature = int(value) * 10  # simulate
        humidity = 50  # simulate
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

# === GUI Setup ===
pygame.init()
screen = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
pygame.display.set_caption("STM32MP1 ENV Dashboard")

font_big = pygame.font.SysFont("Consolas", 36, bold=True)
font_small = pygame.font.SysFont("Consolas", 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
RED = (255, 50, 50)
GREEN = (0, 255, 0)

def draw_text(text, x, y, color, font):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (x, y))

def draw_dashboard(temp, hum, gas, anomaly):
    screen.fill(BLACK)
    draw_text("STM32MP1 ENV MONITOR", 40, 10, CYAN, font_small)
    draw_text(f"TEMP:     {temp} °C", 60, 70, WHITE, font_big)
    draw_text(f"HUMIDITY: {hum} %", 60, 130, WHITE, font_big)
    draw_text(f"GAS:      {gas}", 60, 190, WHITE, font_big)

    if anomaly:
        draw_text("⚠ ANOMALY DETECTED!", 40, 250, RED, font_big)
    else:
        draw_text("✔ STATUS: NORMAL", 60, 250, GREEN, font_big)

    pygame.display.flip()

# === Main Loop ===
last_update = 0
running = True
while running:
    now = time.time()
    if now - last_update > 2:
        temp, hum = read_dht11()
        gas = read_mq135()
        anomaly = detect_anomaly(temp, gas)
        draw_dashboard(temp, hum, gas, anomaly)
        last_update = now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            running = False  # touch to exit

pygame.quit()
