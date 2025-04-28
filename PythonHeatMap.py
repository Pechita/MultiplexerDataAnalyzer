import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import simpledialog
import re
import time
import csv
import os

# ==================== SETTINGS GUI ====================

def get_parameters():
    param_window = tk.Tk()
    param_window.title("Simulation Parameters")

    entries = {}

    defaults = {
        "Serial Port (e.g., COM3)": "COM3",
        "Baud Rate": "9600",
        "Refresh Interval (ms)": "100",
        "Max Duration (seconds)": "60",
        "Average Window (turns)": "30",
        "Save File Name": "sensor_data"
    }

    row = 0
    for label_text, default_value in defaults.items():
        label = tk.Label(param_window, text=label_text)
        label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = tk.Entry(param_window)
        entry.insert(0, default_value)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries[label_text] = entry
        row += 1

    def submit():
        for key in defaults.keys():
            defaults[key] = entries[key].get()
        param_window.destroy()

    submit_button = tk.Button(param_window, text="Start Simulation", command=submit)
    submit_button.grid(row=row, column=0, columnspan=2, pady=10)

    param_window.mainloop()

    return defaults

# Get parameters
params = get_parameters()

# Parse parameters
SERIAL_PORT = params["Serial Port (e.g., COM3)"]
BAUD_RATE = int(params["Baud Rate"])
REFRESH_INTERVAL = int(params["Refresh Interval (ms)"])
MAX_DURATION_SECONDS = int(params["Max Duration (seconds)"])
AVG_WINDOW = int(params["Average Window (turns)"])
SAVE_FILENAME = params["Save File Name"]

# ==================== SERIAL SETUP ====================
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
ser.flush()

# ==================== DATA STORAGE ====================
start_time = time.monotonic()
elapsed_time = 0
history = [[] for _ in range(16)]
time_stamps = []  # Save timestamps
turn_count = 0
recording_done = False  # New flag to stop extra saving

# ==================== PLOT SETUP ====================
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 15))

# --- Instantaneous Heatmap
heatmap = ax1.imshow(np.zeros((4, 4)), cmap='viridis', vmin=0, vmax=5)
cbar1 = plt.colorbar(heatmap, ax=ax1)
ax1.set_title("Instantaneous Photoresistor Voltages")
ax1.set_xlabel("X-axis")
ax1.set_ylabel("Y-axis")

for i in range(4):
    for j in range(4):
        ax1.text(j, i, f"C{4*i+j}", ha="center", va="center", color="white", fontsize=8)

# --- Time Series
lines = []
colors = plt.cm.tab20(np.linspace(0, 1, 16))
for i in range(16):
    line, = ax2.plot([], [], label=f"C{i}", color=colors[i])
    lines.append(line)

ax2.set_ylim(0, 5)
ax2.set_title('Channel Voltages Over Time')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Voltage (V)')
ax2.legend(ncol=4, fontsize="small")
ax2.grid(True)

# --- Averaged Heatmap
avg_heatmap = ax3.imshow(np.zeros((4, 4)), cmap='plasma', vmin=0, vmax=5)
cbar2 = plt.colorbar(avg_heatmap, ax=ax3)
ax3.set_title(f"Averaged Voltages Over Recording")
ax3.set_xlabel("X-axis")
ax3.set_ylabel("Y-axis")

# ==================== FUNCTIONS ====================

def parse_data(line):
    matches = re.findall(r"V\d+=(\d+\.\d)V", line)
    if len(matches) == 16:
        values = [float(m) for m in matches]
        array_4x4 = np.array(values).reshape((4, 4))
        return values, array_4x4
    else:
        return None, None

def save_data():
    folder = "saved_data"
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/{SAVE_FILENAME}.csv"
    print(f"Saving data to {filename}...")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Header
        header = ["Turn", "Timestamp (s)"] + [f"C{i}" for i in range(16)]
        writer.writerow(header)
        # Rows
        for idx in range(len(time_stamps)):
            row = [idx, time_stamps[idx]] + [history[ch][idx] if idx < len(history[ch]) else '' for ch in range(16)]
            writer.writerow(row)
    print("Data saved successfully!")

def update(frame):
    global turn_count, elapsed_time, recording_done

    if recording_done:
        return  # Don't do anything if already finished

    elapsed_time = time.monotonic() - start_time

    if elapsed_time >= MAX_DURATION_SECONDS:
        print(f"Max time ({MAX_DURATION_SECONDS}s) reached. Stopping...")
        ser.close()
        save_data()
        print("Recording finished. Graphs will stay open. Close them manually when done.")
        recording_done = True
        return

    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        print(line)
        values, data = parse_data(line)

        if values is not None:
            # --- Update Instantaneous Heatmap ---
            heatmap.set_data(data)
            heatmap.set_clim(vmin=0, vmax=5)

            # --- Update History ---
            for i in range(16):
                history[i].append(values[i])

            time_stamps.append(elapsed_time)

            turn_count += 1

            # --- Update Time Series Plot ---
            for idx, line in enumerate(lines):
                line.set_data(time_stamps, history[idx])

            ax2.set_xlim(0, max(time_stamps))

            # --- Update Averaged Heatmap ---
            avg_values = []
            for i in range(16):
                avg = np.mean(history[i]) if history[i] else 0
                avg_values.append(avg)
            avg_data = np.array(avg_values).reshape((4, 4))
            avg_heatmap.set_data(avg_data)
            avg_heatmap.set_clim(vmin=0, vmax=5)

ani = animation.FuncAnimation(fig, update, interval=REFRESH_INTERVAL)
plt.tight_layout()
plt.show()
