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

const char* ssid = "CaravanaNet";
const char* password = "caravana2024";
const char* serverName = "http://192.168.43.251:5000";
IPAddress ip; 

void setup() {
  gpsSerial.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);
  dht.begin();
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);  // Tentando conectar ao WiFi
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    String ssid = WiFi.SSID();
    ip = WiFi.localIP();
    char ipStr[16];
    sprintf(ipStr, "%d.%d.%d.%d", ip[0], ip[1], ip[2], ip[3]);
    long rssi = WiFi.RSSI();

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      // Falha ao ler do sensor DHT
      return;
    }

    // Variáveis padrão para os dados do GPS
    /*String latitude = "N/A";
    String longitude = "N/A";
    String altitude = "N/A";
    String velocidade = "N/A";
    String satelites = "N/A";
    String precisao = "N/A";*/

    float latitude = 0;
    float altitude = 0;
    float longitude = 0;
    float velocidade = 0;
    float satelites = 0;
    float precisao = 0;


    // Ler dados do GPS se disponíveis
    while (gpsSerial.available() > 0) {
      if (gps.encode(gpsSerial.read())) {
        if (gps.location.isValid()) {
          float latitude = gps.location.lat();
          float longitude = gps.location.lng();
          float altitude = gps.altitude.meters();
          float velocidade = gps.speed.mps();
          float satelites = gps.satellites.value();
          float precisao = gps.hdop.value();
        }
      }
    }

    // Criar a string httpRequestData com os dados disponíveis
    String httpRequestData = "temperature=" + String(t) + "&humidity=" + String(h) +
                             "&latitude=" + latitude +
                             "&longitude=" + longitude +
                             "&altitude=" + altitude + 
                             "&velocidade=" + velocidade +
                             "&satelites=" + satelites +
                             "&precisao=" + precisao +
                             "&ssid=" + ssid + 
                             "&ip=" + String(ipStr) +
                             "&rssi=" + String(rssi, 4);

    // Enviar a requisição
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    int httpResponseCode = http.POST(httpRequestData);

    if (httpResponseCode <= 0) {
      // Erro ao enviar POST
    }

    http.end();
  } else {
    // WiFi Desconectado
  }
  
  delay(1000);
}
