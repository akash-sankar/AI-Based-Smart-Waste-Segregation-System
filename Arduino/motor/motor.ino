#include <ESP32Servo.h>

// Pin definitions (ESP32)
#define IR_PIN 4
#define BIN_SERVO_PIN 18
#define SEG_SERVO_PIN 19

Servo binServo;
Servo segServo;

int irState = 0;
int serialData = 0;

void setup() {
  Serial.begin(9600);

  pinMode(IR_PIN, INPUT);

  // Set PWM frequency for ESP32 servos
  binServo.setPeriodHertz(50);
  segServo.setPeriodHertz(50);

  binServo.attach(BIN_SERVO_PIN, 500, 2400);
  segServo.attach(SEG_SERVO_PIN, 500, 2400);

  // Initial positions
  binServo.write(110);   // Bin closed
  segServo.write(75);    // Neutral position

  Serial.println("ESP32 Waste Segregation System Ready");
}

void loop() {

  irState = digitalRead(IR_PIN);
  Serial.print("IR Sensor Status: ");
  Serial.println(irState);

  if (Serial.available() > 0) {

    serialData = Serial.parseInt();

    Serial.print("Received Command: ");
    Serial.println(serialData);

    if (serialData == 1) {
      segregateAndDrop(0, 180);
    }
    else if (serialData == 2) {
      segregateAndDrop(75, 180);
    }
    else if (serialData == 3) {
      segregateAndDrop(180, 0);
    }
    else {
      Serial.println("Invalid Command");
    }
  }

  delay(500);
}

void segregateAndDrop(int segAngle, int binAngle) {

  Serial.print("Moving Seg Servo to: ");
  Serial.println(segAngle);
  segServo.write(segAngle);

  delay(3000);

  Serial.println("Opening Bin");
  binServo.write(binAngle);
  delay(2000);

  Serial.println("Closing Bin");
  binServo.write(110);
  delay(1000);
}