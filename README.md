# MultiplexerDataAnalyzer
📖 README: Photoresistor Multiplexer Data Visualization Project
Overview
This project simulates a photoresistor array being read through a multiplexer (MUX) and visualizes the results in real time.
It is designed to test and demonstrate how voltage readings from multiple photoresistors could be monitored, analyzed, and recorded for further research or analysis.

The system has three main parts:

ArduinoFakeData16Reads.ino — Arduino code that simulates reading 16 photoresistors and sends fake voltage values.

PythonHeatMap.py — Python program that connects to the Arduino, reads incoming Serial data live, graphs it in real time, and saves the data.

HeatMapDataReader.py — Python program that reads the saved .csv data file later and displays the graphs again offline.

Files and Their Roles
1. ArduinoFakeData16Reads.ino
Simulates 16 photoresistor voltage readings (0–5V).

Sends data to Serial in the format:
V1=2.3V,V2=1.5V,V3=4.9V,...,V16=3.1V

Randomizes the data every few seconds to imitate real environmental changes.

2. PythonHeatMap.py
Connects to the Arduino over Serial.

Reads and parses incoming fake photoresistor data.

Displays three real-time live graphs:

Heatmap of instantaneous voltages (4x4 grid).

Time series graph of all channel voltages vs time.

Heatmap of averaged voltages across the whole recording.

Asks for important settings (COM Port, Baud Rate, Duration, Save File Name) before starting.

Automatically saves all voltage data to a .csv file when the recording ends.

Graphs stay open after recording finishes.

3. HeatMapDataReader.py
Opens a previously saved .csv data file.

Displays:

Heatmap of the first snapshot (starting readings).

Full time series of all channel voltages vs time.

Heatmap of average voltages across the entire recording.

Lets you analyze old data without needing the Arduino connected.

How to Use
Upload ArduinoFakeData16Reads.ino to your Arduino.

Run PythonHeatMap.py on your computer.

Fill in the Serial Port, Baud Rate, Duration, and Save File Name in the settings window.

Watch the graphs update live.

Data is automatically saved to /saved_data/.

To review saved data later:

Run HeatMapDataReader.py.

It will replot the graphs based on the saved .csv file.

📜 README Update: New Files Added
📂 New Files:
1. HeatMapDataReaderV2.py
Description:

Loads a recorded .csv data file containing voltage readings from a MUX-controlled photoresistor array.

Automatically detects the layout (e.g., 4×4, 16×2, etc.).

Opens three graphs simultaneously:

Averaged Heatmap: Mean voltage across entire recording for each sensor.

Full Time Series Plot: Voltage vs. time for all channels across the whole duration.

Interactive Heatmap Replay: A heatmap that updates manually based on time steps.

Provides a manual "Previous" and "Next" button to step through the recording frame-by-frame.

Allows the user to set a custom "Seconds per Click" to control how fast they navigate through time.

Main New Features:

Simultaneous opening of all graphs (no closing needed between them).

Manual step-through replay (instead of automatic animation).

Customizable time stepping (e.g., 5 seconds per click).

Clear indication of current time on heatmap title.

2. HeatMapReaderV_2.py
Description:

Handles incoming real-time data from Arduino or simulated readings.

Updated to:

Allow dynamic selection of grid layout (rows × columns) at startup.

Let user set colorbar minimum and maximum voltage values.

Allow flexible configuration of recording parameters (duration, refresh rate, save file name).

Improved save functionality:

After the recording ends, the user manually picks where and how to save the .csv file.

No automatic saving into pre-defined folders.

Only plots the live real-time heatmap during acquisition to focus on real-time performance.

Main New Features:

Clean startup GUI for easy parameter setup.

Manual file saving after data recording (no forced folders).

Live updating heatmap with flexible dimensions (any MUX configuration like 4×4, 8×2, 16×2, etc.).

Safely handles faulty data without crashing.

📋 In Summary:

File	Purpose
HeatMapDataReaderV2.py	Analyze and visualize saved data: averaged heatmap, full time series, manual replay navigation
HeatMapReaderV_2.py	Live real-time reading and visualization from Arduino or simulator, with manual saving
