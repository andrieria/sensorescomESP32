#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <MPU6050.h>

const char* ssid = "Dantas_5G";
const char* password = "andri6403";
const char* serverUrl = "http://192.168.1.7:5000/data"; // Substitua SEU_ENDERECO_IP pelo IP do servidor Flask

MPU6050 mpu;

void setup() {
    Serial.begin(9600);
    Wire.begin();
    mpu.initialize();

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Conectando ao WiFi...");
    }

    Serial.println("Conectado ao WiFi");
}

void loop() {
    int16_t ax, ay, az;
    mpu.getAcceleration(&ax, &ay, &az);

    int xpos = map(ax, -17000, 17000, -90, 90);
    int ypos = map(ay, -17000, 17000, -90, 90);

    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverUrl);

        http.addHeader("Content-Type", "application/x-www-form-urlencoded");

        String httpRequestData = "xpos=" + String(xpos) + "&ypos=" + String(ypos);
        int httpResponseCode = http.POST(httpRequestData);

        if (httpResponseCode > 0) {
            Serial.println("Dados enviados com sucesso");
        } else {
            Serial.println("Erro ao enviar os dados: " + String(httpResponseCode));
        }

        http.end();
    }

    delay(100);  // ajuste conforme necessário
}
