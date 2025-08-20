# PPG Collection Tutorial

##### Initialization (you only need to do this once)

Tow this whole folder under your `Arduino` folder

###### Download the library for MAX30102

Go to the folder in your computer named `Arduino`, then go to the subfolder named `libraries`, or use the following command in your terminal.

``````
cd ~/Documents/Arduino/libraries/
``````

Open the terminal and use the following command to download the library

``````
git clone https://github.com/DFRobot/DFRobot_MAX30102.git
``````

##### Download Code to the Board

Open the arduino script named `PPGcollect.ino`, connect it with the board and tap upload

##### Use Python code to save the results

In the folder where you put the python code

`````
python ppg_serial_logger.py
`````

Then it will create a folder called `dataset`, and the csv files will be put there.

##### Notes

This should work fine with a normal Arduino and is suggested to work with Arudino 33 BLE. Please let me know if you want to use other Arduino boards to collect data, should be a easy change. 

``````
MAX30102    →    Arduino
VCC         →    3.3V
GND         →    GND
SDA         →    A4 (Uno) or SDA
SCL         →    A5 (Uno) or SCL
``````

**On different Arduinos:**

- **Arduino Uno/Nano**: SDA=A4, SCL=A5
- **Arduino Mega**: SDA=20, SCL=21
- **ESP32**: Usually GPIO 21=SDA, GPIO 22=SCL
- **Arduino Nano 33**: A4=SDA, A5=SCL