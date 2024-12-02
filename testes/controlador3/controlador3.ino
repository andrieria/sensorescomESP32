#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <TinyGPS++.h>
#include <Wire.h>
#include <MPU6050.h>

#define DHTPIN 33     // Pino onde o DHT11 está conectado
#define DHTTYPE DHT11 // Tipo de sensor DHT11
#define RX_PIN 16     // Pino RX2 do ESP32 conectado ao TX do GPS
#define TX_PIN 17     // Pino TX2 do ESP32 conectado ao RX do GPS

DHT dht(DHTPIN, DHTTYPE);
TinyGPSPlus gps;
MPU6050 mpu;

HardwareSerial gpsSerial(2);  // Cria uma instância de HardwareSerial para o GPS (Serial2)

const char* ssid = "andrieriawifi";
const char* password = "dridrigata";
const char* serverName = "http://192.168.132.251:5000";

void setup() {
  // Inicializa a porta serial do GPS
  gpsSerial.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);

  // Inicializa o DHT11
  dht.begin();
  
  // Conecta ao WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  // Inicializa o MPU6050
  Wire.begin();
  mpu.initialize();
  
  // Verifica a conexão com o MPU6050
  if (!mpu.testConnection()) {
    // Falha ao conectar com o MPU6050
    return;
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    
    // Inicializa o HTTPClient
    HTTPClient http;
    http.begin(serverName);

    // Leitura dos dados do sensor DHT11
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    
    if (isnan(h) || isnan(t)) {
      // Falha ao ler do sensor DHT
      return;
    }

    // Leitura dos dados do GPS
    while (gpsSerial.available() > 0) {
      if (gps.encode(gpsSerial.read())) {
        if (gps.location.isValid()) {
          float latitude = gps.location.lat();
          float longitude = gps.location.lng();
          float altitude = gps.altitude.meters();
          float velocidade = gps.speed.mps();
          float satelites = gps.satellites.value();
          float precisao = gps.hdop.value();

          // Leitura dos dados do acelerômetro e giroscópio do MPU6050
          int16_t ax, ay, az, gx, gy, gz;
          mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

          // Montando a string com todos os dados
          String httpRequestData = "temperature=" + String(t) + "&humidity=" + String(h) +
                                   "&latitude=" + String(latitude, 6) +
                                   "&longitude=" + String(longitude, 6) +
                                   "&altitude=" + String(altitude, 2) + 
                                   "&velocidade=" + String(velocidade, 3) +
                                   "&satelites=" + String(satelites, 5) +
                                   "&precisao=" + String(precisao, 6) +
                                   "&ax=" + String(ax) +
                                   "&ay=" + String(ay) +
                                   "&az=" + String(az) +
                                   "&gx=" + String(gx) +
                                   "&gy=" + String(gy) +
                                   "&gz=" + String(gz);

          // Envia os dados via HTTP POST
          http.addHeader("Content-Type", "application/x-www-form-urlencoded");
          int httpResponseCode = http.POST(httpRequestData);
          
          if (httpResponseCode <= 0) {
            // Erro ao enviar POST
          }

          http.end(); // Fecha a conexão HTTP
        }
      }
    }
  } else {
    // WiFi Desconectado
  }
  
  delay(1000); // Aguarda 1 segundo antes de enviar os dados novamente
}
