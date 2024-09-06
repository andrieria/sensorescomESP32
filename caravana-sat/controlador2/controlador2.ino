#include <Wire.h>
#include <MPU6050.h> // Biblioteca do sensor MPU6050
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <TinyGPS++.h>

#define DHTPIN 33     // Pino onde o DHT11 está conectado
#define DHTTYPE DHT11   // Tipo de sensor DHT11
#define RX_PIN 16    // Pino RX2 do ESP32 conectado ao TX do GPS
#define TX_PIN 17    // Pino TX2 do ESP32 conectado ao RX do GPS
#define MPU_SDA 21   // Pino SDA do MPU6050
#define MPU_SCL 22   // Pino SCL do MPU6050

DHT dht(DHTPIN, DHTTYPE);
TinyGPSPlus gps;
HardwareSerial gpsSerial(2);  // Cria uma instância de HardwareSerial para o GPS (Serial2)
MPU6050 mpu;  // Instância do sensor MPU6050

const char* ssid = "CaravanaNet";
const char* password = "caravana2024";
const char* serverName = "http://192.168.132.251:5000";
IPAddress ip; 

void setup() {
  gpsSerial.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);
  dht.begin();

  Wire.begin(MPU_SDA, MPU_SCL);  // Inicializa o barramento I2C com os pinos definidos
  mpu.initialize();  // Inicializa o MPU6050
  
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
    long rssi = WiFi.RSSI();

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      // Falha ao ler do sensor DHT
      return;
    }

    float latitude = 0;
    float altitude = 0;
    float longitude = 0;
    float velocidade = 0;
    float satelites = 0;
    float precisao = 0;

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

    // Dados do MPU6050
    int16_t ax, ay, az;
    int16_t gx, gy, gz;
    mpu.getAcceleration(&ax, &ay, &az);
    mpu.getRotation(&gx, &gy, &gz);

    // Criar a string httpRequestData com os dados disponíveis
    String httpRequestData = "temperature=" + String(t) + "&humidity=" + String(h) +
                             "&latitude=" + latitude +
                             "&longitude=" + longitude +
                             "&altitude=" + altitude + 
                             "&velocidade=" + velocidade +
                             "&satelites=" + satelites +
                             "&precisao=" + precisao +
                             "&ssid=" + ssid + 
                             "&ip=" + String(ip, 15) +
                             "&rssi=" + String(rssi, 4) +
                             "&acc_x=" + String(ax) +
                             "&acc_y=" + String(ay) +
                             "&acc_z=" + String(az) +
                             "&gyro_x=" + String(gx) +
                             "&gyro_y=" + String(gy) +
                             "&gyro_z=" + String(gz);

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
