#include <Wire.h>
#include "DFRobot_MAX30102.h"

DFRobot_MAX30102 particleSensor;

void setup() {
  Serial.begin(115200);
  Serial.println("MAX30102 Heart Rate & SpO2 Data Collection");
  
  // Initialize sensor
  if (!particleSensor.begin()) {
    Serial.println("Sensor not found! Check wiring.");
    while(1);
  }
  
  // Configure sensor (moderate settings for good data quality)
  particleSensor.sensorConfiguration(
    50,              // LED brightness (0-255)
    SAMPLEAVG_4,     // Average 4 samples
    MODE_MULTILED,   // Use both Red and IR LEDs
    SAMPLERATE_100,  // 100 samples per second
    PULSEWIDTH_411,  // Pulse width
    ADCRANGE_16384   // ADC range
  );
  
  Serial.println("Sensor initialized. Place finger on sensor.");
  Serial.println("Time(s),HeartRate(BPM),SpO2(%)");
  
  delay(1000);
}

void loop() {
  // Check if finger is detected
  uint32_t irValue = particleSensor.getIR();
  
  if (irValue > 50000) {  // Finger detected
    // Get heart rate and SpO2
    float heartRate = particleSensor.getHeartRate();
    float spO2 = particleSensor.getSpO2();
    
    // Only output valid readings
    if (heartRate > 30 && heartRate < 200 && spO2 > 70 && spO2 <= 100) {
      // Output: Time in seconds, Heart Rate, SpO2
      Serial.print(millis() / 1000.0, 1);
      Serial.print(",");
      Serial.print(heartRate, 1);
      Serial.print(",");
      Serial.println(spO2, 1);
    }
  } else {
    Serial.println("No finger detected");
  }
  
  delay(1000);  // Read every second
}