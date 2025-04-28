import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========== SETTINGS ==========
FILENAME = "saved_data/sensor_data_4.csv"  # <<<< Set your filename here

# ========== LOAD DATA ==========
data = pd.read_csv(FILENAME)

# Extract useful pieces
timestamps = data['Timestamp (s)']
channels = [f'C{i}' for i in range(16)]
channel_data = data[channels]

# ========== PLOT SETUP ==========

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 15))

# --- First Plot: Instantaneous Heatmap (first data point) ---
first_readings = channel_data.iloc[0].values.reshape((4,4))
heatmap1 = ax1.imshow(first_readings, cmap='viridis', vmin=0, vmax=5)
cbar1 = plt.colorbar(heatmap1, ax=ax1)
ax1.set_title(f"First Snapshot of Voltages")
ax1.set_xlabel("X-axis")
ax1.set_ylabel("Y-axis")

for i in range(4):
    for j in range(4):
        ax1.text(j, i, f"C{4*i+j}", ha="center", va="center", color="white", fontsize=8)

# --- Second Plot: Time Series (all 16 channels) ---
colors = plt.cm.tab20(np.linspace(0, 1, 16))
for idx, ch in enumerate(channels):
    ax2.plot(timestamps, channel_data[ch], label=ch, color=colors[idx])

ax2.set_ylim(0, 5)
ax2.set_title('Channel Voltages Over Time (From File)')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Voltage (V)')
ax2.legend(ncol=4, fontsize="small")
ax2.grid(True)

# --- Third Plot: Averaged Heatmap (average over ALL turns) ---
avg_readings = channel_data.mean().values.reshape((4,4))

heatmap2 = ax3.imshow(avg_readings, cmap='plasma', vmin=0, vmax=5)
cbar2 = plt.colorbar(heatmap2, ax=ax3)
ax3.set_title(f"Averaged Voltages Over ALL {len(data)} Turns")
ax3.set_xlabel("X-axis")
ax3.set_ylabel("Y-axis")

# ========== DISPLAY ==========
plt.tight_layout()
plt.show()
