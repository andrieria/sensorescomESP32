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
const char* serverName = "http://192.168.176.10:5000";

void setup() {
  // Inicializa a porta serial do GPS
  //Serial.begin(9600);

  gpsSerial.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);

  dht.begin();
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    //Serial.println(WiFi.status());
    delay(1000);
    // Tentando conectar ao WiFi
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    //Serial.println(WiFi.localIP());
    
    HTTPClient http;
    http.begin(serverName);

    float latitude = 0;
    float longitude = 0;
    float altitude = 0;
    float velocidade = 0;
    float satelites = 0;
    float precisao = 0;

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
          latitude = gps.location.lat();
          longitude = gps.location.lng();
          altitude = gps.altitude.meters();
          velocidade = gps.speed.mps();
          satelites = gps.satellites.value();
          precisao = gps.hdop.value();

        }
      }
    }


    String httpRequestData = "temperature=" + String(t) + "&humidity=" + String(h) +
                              "&latitude=" + String(latitude, 6) +
                              "&longitude=" + String(longitude, 6) +
                              "&altitude=" + String(altitude, 2) + 
                              "&velocidade=" + String(velocidade, 3) +
                              "&satelites=" + String(satelites, 5) +
                              "&precisao=" + String(precisao, 6);

    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    int httpResponseCode = http.POST(httpRequestData);
          
    if (httpResponseCode <= 0) {
        // Erro ao enviar POST
    }
          
    http.end();
  } else {
    // WiFi Desconectado
    //Serial.println("Desconectado.");
  }
  
  delay(1000); // Envia a cada 60 segundos
}