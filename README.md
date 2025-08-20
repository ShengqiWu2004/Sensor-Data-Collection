# Sensor Data Collection

This repository provides starter code for collecting and storing sensor data with Arduino boards and Python scripts.  
It is designed to be beginner-friendly for users without a computer science background.

## Folder Structure

- **PPGcollect/**  
  Contains Arduino code (`PPGcollect.ino`) and Python script (`ppg_serial_logger.py`) for collecting **PPG (Photoplethysmography)** sensor data.  
  The tutorial for setup and usage is provided in [PPG Collection Tutorial](./PPGcollect/README.md).

- **datasetCollection/**  
  Contains Arduino and Python code for collecting **Acceleration & Gyroscope (IMU)** sensor data.

## Notes

- Please open an issue if you need additional code for other types of sensors or if you require changes such as **sensitivity adjustment**.  
- The code is tested primarily with Arduino Uno, Nano, and Nano 33 BLE. Other boards can be supported with small modifications.

---
