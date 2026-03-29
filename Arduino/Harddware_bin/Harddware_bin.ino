#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

// ================= WIFI =================
const char* ssid = "Project";
const char* password = "12345678";

// ================= SERVER =================
ESP8266WebServer server(80);

// ================= LCD =================
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ================= SERVOS =================
Servo rotateServo;
Servo dropServo;

// ================= PINS =================
#define ROTATE_PIN D5
#define DROP_PIN   D6   // Only one pin needed for servo

// ================= ANGLES =================
int angles[4] = {0, 60, 120, 180};

// ================= FUNCTION =================
void moveSystem(int index) {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("TYPE ");
  lcd.print(index+1);

  // Rotate Servo
  rotateServo.write(angles[index]);
  delay(1000);

  lcd.setCursor(0,1);
  lcd.print("Dropping...");

  // Drop Servo Action
  dropServo.write(135);
  delay(800);
  dropServo.write(90);

  delay(500);

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Done TYPE ");
  lcd.print(index+1);
}

// ================= ROUTES =================
void handleZone1() { moveSystem(0); server.send(200, "text/plain", "Zone1 Done"); }
void handleZone2() { moveSystem(1); server.send(200, "text/plain", "Zone2 Done"); }
void handleZone3() { moveSystem(2); server.send(200, "text/plain", "Zone3 Done"); }
void handleZone4() { moveSystem(3); server.send(200, "text/plain", "Zone4 Done"); }

// ================= SETUP =================
void setup() {
  Serial.begin(9600);

  // LCD Init
  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("System Ready");

  // Servo Init
  rotateServo.attach(ROTATE_PIN);
  dropServo.attach(DROP_PIN);

  dropServo.write(90);  // initial

  // WiFi
  WiFi.begin(ssid, password);
  lcd.setCursor(0,1);
  lcd.print("Connecting...");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  lcd.clear();
  lcd.print("WiFi Connected");

  // Routes
  server.on("/1", handleZone1);
  server.on("/2", handleZone2);
  server.on("/3", handleZone3);
  server.on("/4", handleZone4);

  server.begin();

  Serial.println(WiFi.localIP());
}

// ================= LOOP =================
void loop() {
  server.handleClient();
}
