#include <WiFi.h>
#include <HTTPClient.h>
#include "Wire.h"       
#include "I2Cdev.h"     
#include "MPU6050.h"    

const char* ssid = "JardimTelecom- Adilson_5G";
const char* password = "adoliveira";
const char* serverName = "http://192.168.211.251:5000"; // IP do servidor Flask

MPU6050 mpu;
int16_t ax, ay, az;
int16_t gx, gy, gz;

struct MyData {
  byte X;
  byte Y;
  byte Z;
  byte Gx;
  byte Gy;
  byte Gz;
};

MyData data;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  Wire.begin();
  mpu.initialize();
}

void loop() {
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  data.X = map(ax, -17000, 17000, 0, 2000); 
  data.Y = map(ay, -17000, 17000, 0, 2000); 
  data.Z = map(az, -17000, 17000, 0, 2000); 
  data.Gx = map(gx, -17000, 17000, 0, 2000); 
  data.Gy = map(gy, -17000, 17000, 0, 2000); 
  data.Gz = map(gz, -17000, 17000, 0, 2000);

  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String postData = "X=" + String(data.X) + "&Y=" + String(data.Y) + "&Z=" + String(data.Z) +
                      "&Gx=" + String(data.Gx) + "&Gy=" + String(data.Gy) + "&Gz=" + String(data.Gz);

    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    }
    else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
  delay(100);
}
