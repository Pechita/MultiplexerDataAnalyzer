// Arduino Fake MUX Data Sender

const int numSensors = 16;    // 4x4 grid
float sensorValues[numSensors];

unsigned long lastUpdate = 0;
const unsigned long updateInterval = 2500; // 2.5 seconds (change data)

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A0)); // Seed randomness
  generateRandomValues();
}

void loop() {
  unsigned long currentMillis = millis();

  // If 2.5 seconds passed, generate new random values
  if (currentMillis - lastUpdate >= updateInterval) {
    generateRandomValues();
    lastUpdate = currentMillis;
  }

  // Send sensor values one by one, to simulate MUX scanning
  for (int i = 0; i < numSensors; i++) {
    Serial.print("V");
    Serial.print(i+1);
    Serial.print("=");
    Serial.print(sensorValues[i], 1); // 1 decimal place
    Serial.print("V");
    if (i != numSensors-1) Serial.print(","); // commas between values
  }
  Serial.println(); // end of transmission

  delay(100); // small delay to simulate realistic serial speed
}

void generateRandomValues() {
  for (int i = 0; i < numSensors; i++) {
    sensorValues[i] = random(0, 51) / 10.0; // Random 0.0V to 5.0V
  }
}
