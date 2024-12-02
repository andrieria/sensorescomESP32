/*#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 mpu;
int16_t ax, ay, az;
int16_t gx, gy, gz;

struct MyData {
  float X;
  float Y;
  float Z;
};

MyData data;

void setup()
{
  Serial.begin(115200); // Aumente a taxa de baud para uma transmissão mais rápida
  Wire.begin();
  mpu.initialize();
}

void loop()
{
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  data.X = map(ax, -17000, 17000, 0, 255 ); // Eixo X
  data.Y = map(ay, -17000, 17000, 0, 255); // Eixo Y
  data.Z = map(az, -17000, 17000, 0, 255); // Eixo Z
  
  Serial.print(data.X, 2); // Envia com 2 casas decimais
  Serial.print(" ");
  Serial.print(data.Y, 2);
  Serial.print(" ");
  Serial.println(data.Z, 2);

  delay(10); // Reduz o delay para aumentar a frequência de amostragem
}*/


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
  delay(100);
  Serial.print(data.X);
  Serial.print(" ");
  Serial.print(data.Y);
  Serial.print(" ");
  Serial.println(data.Z);
}