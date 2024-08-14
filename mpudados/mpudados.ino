#include "Wire.h"       
#include "I2Cdev.h"     
#include "MPU6050.h"    

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

void setup()
{
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
  //pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  data.X = map(ax, -17000, 17000, 0, 255 ); 
  data.Y = map(ay, -17000, 17000, 0, 255); 
  data.Z = map(az, -17000, 17000, 0, 255); 
  data.Gx = map(gx, -17000, 17000, 0, 255); 
  data.Gy = map(gy, -17000, 17000, 0, 255); 
  data.Gz = map(gz, -17000, 17000, 0, 255); 
  delay(500);
  Serial.print(data.X);
  Serial.print(" ");
  Serial.print(data.Y);
  Serial.print(" ");
  Serial.print(data.Z);
  Serial.print(" ");
  Serial.print(data.Gx);
  Serial.print(" ");
  Serial.print(data.Gy);
  Serial.print(" ");
  Serial.println(data.Gz);
}







/*#include "Wire.h"       
#include "I2Cdev.h"     
#include "MPU6050.h"    

MPU6050 mpu;
int16_t ax, ay, az;
int16_t gx, gy, gz;

struct MyData {
  byte X;
  byte Y;
  byte Z;
};

MyData data;

void setup()
{
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
  //pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  data.X = map(ax, -17000, 17000, 0, 255 ); // X axis data
  data.Y = map(ay, -17000, 17000, 0, 255); 
  data.Z = map(az, -17000, 17000, 0, 255);  // Y axis data
  delay(500);
  Serial.print(data.X);
  Serial.print(" ");
  Serial.print(data.Y);
  Serial.print(" ");
  Serial.println(data.Z);
}
*/


/*#include <WiFi.h>
#include <Wire.h>
#include "MPU6050.h"

const char* ssid = "andrieriawifi";
const char* password = "dridrigata";
const char* serverName = "http://192.168.4.251:5000/";

MPU6050 mpu;
WiFiClient client;

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
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
    while (1);
  }
}

void loop() {
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  if (client.connect(serverName, 80)) {
    String postData = "ax=" + String(ax) + "&ay=" + String(ay) + "&az=" + String(az) + "&gx=" + String(gx) + "&gy=" + String(gy) + "&gz=" + String(gz);
    
    client.println("POST /data HTTP/1.1");
    client.println("Host: your_flask_server_ip");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.print("Content-Length: ");
    client.println(postData.length());
    client.println();
    client.print(postData);
    
    client.stop();
  }

  delay(100);  // Reduced delay for faster updates
}*/



/*#include <WiFi.h>
#include <Wire.h>
#include "MPU6050.h"

const char* ssid = "andrieriawifi";
const char* password = "dridrigata";
const char* serverName = "http://192.168.4.251:5000";

MPU6050 mpu;
WiFiClient client;

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  Wire.begin();
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
    while (1);
  }
}

void loop() {
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  if (client.connect(serverName, 80)) {
    String postData = "ax=" + String(ax) + "&ay=" + String(ay) + "&az=" + String(az) + "&gx=" + String(gx) + "&gy=" + String(gy) + "&gz=" + String(gz);
    
    client.println("POST /data HTTP/1.1");
    client.println("Host: your_flask_server_ip");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.print("Content-Length: ");
    client.println(postData.length());
    client.println();
    client.print(postData);
    
    client.stop();
  }

  delay(1000);
}*/
