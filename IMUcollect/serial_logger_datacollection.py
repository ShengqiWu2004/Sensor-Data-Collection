import serial
import time
import serial.tools.list_ports
from datetime import datetime

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(port.name)
        print(port.vid)
        # Check for Arduino Nano 33 BLE specifics (adjust VID/PID if necessary)
        if port.vid == 9025:
            return port.device  # Return the COM port (e.g., 'COM6' or '/dev/ttyACM0')
    return None

# Main logic to use the port
port = find_arduino_port()
baudrate = 9600  # Ensure this matches the baud rate in your Arduino code

# Initialize serial connection
try:
    ser = serial.Serial(port, baudrate, timeout=2)
    print(f"Connected to {port} at {baudrate} baud")
except serial.SerialException as e:
    print(f"Error: Could not open serial port {port}. {e}")
    exit()

# Create timestamped CSV file
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f'IMU_Data_{timestamp}.csv'

try:
    with open(output_file, 'w') as file:
        print(f"Saving data to {output_file}...")

        # Continuously read from the serial port
        while True:
            try:
                # Read a line from the Arduino
                line = ser.readline().decode('utf-8').strip()

                # If data is received, save it to the file
                if line:
                    print(f"Received: {line}")
                    file.write(line + '\n')  # Append the data with a newline
                    file.flush()  # Ensure data is written immediately

            except KeyboardInterrupt:
                print("Stopping data capture. Exiting...")
                break

except IOError as e:
    print(f"Error: Could not write to file {output_file}. {e}")

# Close the serial port
finally:
    if ser.is_open:
        ser.close()
        print("Serial port closed.")