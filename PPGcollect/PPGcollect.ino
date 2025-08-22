#include <Wire.h>
#include "DFRobot_MAX30102.h"

DFRobot_MAX30102 particleSensor;

void setup() {
  Serial.begin(115200);
  Serial.println("MAX30102 Heart Rate & SpO2 Data Collection");
  
  // Initialize sensor
  if (!particleSensor.begin()) {
    Serial.println("MAX30102 was not found. Please check wiring/power.");
    while(1);
  }
  
  // Configure sensor (using the actual API signature)
  particleSensor.sensorConfiguration(
    60,              // LED brightness (0-255, default 0x1F=31)
    SAMPLEAVG_4,     // Average 4 samples
    MODE_MULTILED,   // Use both Red and IR LEDs
    SAMPLERATE_100,  // 100 samples per second (changed from 400 to reduce data rate)
    PULSEWIDTH_411,  // Pulse width
    ADCRANGE_4096    // ADC range (default is 4096, not 16384)
  );
  
  Serial.println("Sensor initialized. Place finger on sensor.");
  Serial.println("Time(s),IR_Raw,Red_Raw,HeartRate(BPM),HR_Valid,SpO2(%),SpO2_Valid,Status");
  
  delay(2000); // Give sensor time to stabilize
}

void loop() {
  // Get raw values
  uint32_t irValue = particleSensor.getIR();
  uint32_t redValue = particleSensor.getRed();
  
  // Variables for heart rate and SpO2 calculation
  int32_t spo2;
  int8_t spo2Valid;
  int32_t heartRate;
  int8_t heartRateValid;
  
  // Check if finger is detected
  bool fingerDetected = irValue > 50000;
  
  if (fingerDetected) {
    // Calculate heart rate and SpO2 using built-in algorithm
    particleSensor.heartrateAndOxygenSaturation(&spo2, &spo2Valid, &heartRate, &heartRateValid);
    
    // Output data every second
    static uint32_t lastOutput = 0;
    if (millis() - lastOutput >= 1000) {
      lastOutput = millis();
      
      // Output: Time, IR Raw, Red Raw, Heart Rate, HR Valid, SpO2, SpO2 Valid, Status
      Serial.print(millis() / 1000.0, 1);
      Serial.print(",");
      Serial.print(irValue);
      Serial.print(",");
      Serial.print(redValue);
      Serial.print(",");
      
      // Heart Rate
      if (heartRateValid) {
        Serial.print(heartRate);
      } else {
        Serial.print("---");
      }
      Serial.print(",");
      Serial.print(heartRateValid ? "1" : "0");
      Serial.print(",");
      
      // SpO2
      if (spo2Valid) {
        Serial.print(spo2);
      } else {
        Serial.print("---");
      }
      Serial.print(",");
      Serial.print(spo2Valid ? "1" : "0");
      Serial.print(",");
      
      // Status
      if (heartRateValid && spo2Valid) {
        Serial.println("GOOD");
      } else if (heartRateValid || spo2Valid) {
        Serial.println("PARTIAL");
      } else {
        Serial.println("CALCULATING");
      }
    }
    
  } else {
    // No finger detected
    static uint32_t lastNoFingerOutput = 0;
    if (millis() - lastNoFingerOutput >= 2000) { // Output less frequently when no finger
      lastNoFingerOutput = millis();
      
      Serial.print(millis() / 1000.0, 1);
      Serial.print(",");
      Serial.print(irValue);
      Serial.print(",");
      Serial.print(redValue);
      Serial.println(",---,0,---,0,NO_FINGER");
    }
  }
  
  delay(100); // Small delay to prevent overwhelming the sensor
}

// Alternative simplified version for CSV output only
/*
void loop() {
  uint32_t irValue = particleSensor.getIR();
  
  if (irValue > 50000) {  // Finger detected
    int32_t spo2, heartRate;
    int8_t spo2Valid, heartRateValid;
    
    particleSensor.heartrateAndOxygenSaturation(&spo2, &spo2Valid, &heartRate, &heartRateValid);
    
    // Only output when both values are valid
    if (heartRateValid && spo2Valid && heartRate > 30 && heartRate < 200 && spo2 > 70 && spo2 <= 100) {
      Serial.print(millis() / 1000.0, 1);
      Serial.print(",");
      Serial.print(heartRate);
      Serial.print(",");
      Serial.println(spo2);
    }
  }
  
  delay(1000);
}
*/