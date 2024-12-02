#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
    Serial.begin(9600);
    Wire.begin();
    mpu.initialize();
}

void loop() {
    int16_t ax, ay, az;
    mpu.getAcceleration(&ax, &ay, &az);

    int xpos = map(ax, -17000, 17000, -90, 90);
    int ypos = map(ay, -17000, 17000, -90, 90);

    // Enviar os dados como uma string para o Python via serial
    Serial.print(xpos);
    Serial.print(" ");
    Serial.println(ypos);

    delay(100);  // ajuste conforme necessário
}
