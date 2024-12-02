#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <TinyGPS++.h>

#define DHTPIN 33     // Pino onde o DHT11 está conectado
#define DHTTYPE DHT11   // Tipo de sensor DHT11
#define RX_PIN 16    // Pino RX2 do ESP32 conectado ao TX do GPS
#define TX_PIN 17    // Pino TX2 do ESP32 conectado ao RX do GPS

DHT dht(DHTPIN, DHTTYPE);
TinyGPSPlus gps;
HardwareSerial gpsSerial(2);  // Cria uma instância de HardwareSerial para o GPS (Serial2)

const char* ssid = "andrieriawifi";
const char* password = "dridrigata";
const char* serverName = "http://192.168.132.251:5000";

void setup() {
  // Inicializa a porta serial do GPS
  gpsSerial.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);

  dht.begin();
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    // Tentando conectar ao WiFi
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      // Falha ao ler do sensor DHT
      return;
    }

    // Ler dados do GPS
    while (gpsSerial.available() > 0) {
      if (gps.encode(gpsSerial.read())) {
        if (gps.location.isValid()) {
          float latitude = gps.location.lat();
          float longitude = gps.location.lng();
          float altitude = gps.altitude.meters();

          String httpRequestData = "temperature=" + String(t) + "&humidity=" + String(h) +
                                   "&latitude=" + String(latitude, 6) +
                                   "&longitude=" + String(longitude, 6) +
                                   "&altitude=" + String(altitude, 2);

          http.addHeader("Content-Type", "application/x-www-form-urlencoded");

          int httpResponseCode = http.POST(httpRequestData);
          
          if (httpResponseCode <= 0) {
            // Erro ao enviar POST
          }
          
          http.end();
        }
      }
    }
  } else {
    // WiFi Desconectado
  }
  
  delay(60000); // Envia a cada 60 segundos
}
