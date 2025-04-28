# MultiplexerDataAnalyzer
📖 README: Photoresistor Multiplexer Data Visualization Project
Overview
This project simulates a photoresistor array being read through a multiplexer (MUX) and visualizes the results in real time.
It is designed to test and demonstrate how voltage readings from multiple photoresistors could be monitored, analyzed, and recorded for further research or analysis.

The system has three main parts:

ArduinoFakeDataReads.ino — Arduino code that simulates reading 16 photoresistors and sends fake voltage values.

PythonHeatMap.py — Python program that connects to the Arduino, reads incoming Serial data live, graphs it in real time, and saves the data.

HeatMapDataReader.py — Python program that reads the saved .csv data file later and displays the graphs again offline.

Files and Their Roles
1. ArduinoFakeDataReads.ino
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
Upload ArduinoFakeDataReads.ino to your Arduino.

Run PythonHeatMap.py on your computer.

Fill in the Serial Port, Baud Rate, Duration, and Save File Name in the settings window.

Watch the graphs update live.

Data is automatically saved to /saved_data/.

To review saved data later:

Run HeatMapDataReader.py.

It will replot the graphs based on the saved .csv file.

