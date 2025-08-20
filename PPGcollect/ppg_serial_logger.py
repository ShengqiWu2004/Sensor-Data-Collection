import serial
import time
import serial.tools.list_ports
from datetime import datetime
import csv
import os

def find_arduino_port():
    """Find the Arduino port automatically"""
    ports = list(serial.tools.list_ports.comports())
    print("Available ports:")
    
    for port in ports:
        print(f"  {port.device} - {port.description}")
        # Check for common Arduino identifiers
        if (port.vid == 9025 or  # Arduino Nano 33 BLE
            port.vid == 0x2341 or  # Standard Arduino VID
            'Arduino' in port.description or
            'CH340' in port.description or  # Common USB-to-serial chip
            'CP210' in port.description):   # Another common chip
            print(f"Found potential Arduino at: {port.device}")
            return port.device
    
    # If no Arduino found automatically, show all ports
    print("\nNo Arduino automatically detected. Available ports:")
    for i, port in enumerate(ports):
        print(f"  {i}: {port.device} - {port.description}")
    
    # Let user choose manually
    if ports:
        choice = input(f"Enter port number (0-{len(ports)-1}) or press Enter to try COM3: ")
        if choice.strip():
            return ports[int(choice)].device
        else:
            return "COM3"  # Default fallback
    
    return None

def create_timestamped_filename():
    """Create filename with current date/time in dataset folder"""
    # Create dataset directory if it doesn't exist
    dataset_dir = "./dataset"
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        print(f"Created directory: {dataset_dir}")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename = f'ppg_data_{timestamp}.csv'
    return os.path.join(dataset_dir, filename)

def parse_ppg_data(line):
    """Parse the PPG data line and return components"""
    try:
        # Expected format: "Time(s),HeartRate(BPM),SpO2(%)"
        if ',' in line and not line.startswith('Time') and 'No finger' not in line:
            parts = line.split(',')
            if len(parts) >= 3:
                arduino_time = float(parts[0])
                heart_rate = float(parts[1])
                spo2 = float(parts[2])
                return arduino_time, heart_rate, spo2
    except (ValueError, IndexError):
        pass
    return None

def main():
    # Find Arduino port
    port = find_arduino_port()
    if not port:
        print("No Arduino port found!")
        return
    
    baudrate = 115200  # Match Arduino code baudrate
    
    # Initialize serial connection
    try:
        ser = serial.Serial(port, baudrate, timeout=2)
        print(f"Connected to {port} at {baudrate} baud")
        time.sleep(2)  # Wait for Arduino to initialize
    except serial.SerialException as e:
        print(f"Error: Could not open serial port {port}. {e}")
        return
    
    # Create timestamped CSV file
    output_file = create_timestamped_filename()
    
    print(f"Saving PPG data to {output_file}...")
    print("Place finger on sensor and wait for readings...")
    print("Press Ctrl+C to stop data collection")
    
    try:
        with open(output_file, 'w', newline='') as file:
            # Create CSV writer
            writer = csv.writer(file)
            
            # Write header
            header = ['Timestamp', 'Arduino_Time_s', 'HeartRate_BPM', 'SpO2_Percent']
            writer.writerow(header)
            print(f"CSV header: {', '.join(header)}")
            
            # Skip initial Arduino startup messages
            startup_lines = 0
            while startup_lines < 10:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        print(f"Arduino: {line}")
                        startup_lines += 1
                        if "Place finger" in line or "Time(s)" in line:
                            break
                except:
                    pass
            
            print("\nStarting data collection...")
            data_count = 0
            
            # Continuously read from the serial port
            while True:
                try:
                    # Read a line from the Arduino
                    line = ser.readline().decode('utf-8').strip()
                    
                    if line:
                        print(f"Received: {line}")
                        
                        # Parse PPG data
                        parsed_data = parse_ppg_data(line)
                        
                        if parsed_data:
                            arduino_time, heart_rate, spo2 = parsed_data
                            
                            # Get current timestamp with high precision
                            now = datetime.now()
                            timestamp_full = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Remove last 3 digits for milliseconds
                            
                            # Write to CSV
                            row = [timestamp_full, arduino_time, heart_rate, spo2]
                            writer.writerow(row)
                            file.flush()  # Ensure data is written immediately
                            
                            data_count += 1
                            print(f"  -> Saved data point #{data_count}: HR={heart_rate}, SpO2={spo2}%")
                        
                        elif "No finger" in line:
                            print("  -> Waiting for finger detection...")
                
                except UnicodeDecodeError:
                    print("  -> Received non-text data (skipping)")
                    continue
                
                except KeyboardInterrupt:
                    print(f"\nStopping data capture. Collected {data_count} data points.")
                    break
                
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    continue
    
    except IOError as e:
        print(f"Error: Could not write to file {output_file}. {e}")
    
    finally:
        # Close the serial port
        if ser.is_open:
            ser.close()
            print("Serial port closed.")
        
        # Show file info
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"\nData saved to: {output_file}")
            print(f"File size: {file_size} bytes")
            print(f"Total data points collected: {data_count}")

if __name__ == "__main__":
    main()