#include <DHT.h>          // Biblioteca para o sensor DHT11
#include <TinyGPS++.h>    // Biblioteca para o módulo GPS
//#include <SoftwareSerial.h>
#include <ArduinoJson.h>

#define DHTPIN 4         // Pino ao qual o sensor DHT11 está conectado
#define DHTTYPE DHT11    // Tipo do sensor DHT

//#define RXPin 18          // Pino RX do módulo GPS
//#define TXPin 19         // Pino TX do módulo GPS

DHT dht(DHTPIN, DHTTYPE);   // Inicialização do objeto DHT
TinyGPSPlus gps;            // Inicialização do objeto TinyGPS++
//SoftwareSerial gpsSerial(RXPin, TXPin);  // Inicialização da comunicação serial para o módulo GPS

void setup() {
  Serial.begin(9600);       // Inicialização da comunicação serial com o computador
  //gpsSerial.begin(9600);     // Inicialização da comunicação serial com o módulo GPS
  dht.begin();               // Inicialização do sensor DHT11
   
}

void showGPSData() {
  if (gps.location.isValid()) {
    Serial1.print("Latitude: ");
    Serial1.print(gps.location.lat(), 6);
    Serial1.print(" | Longitude: ");
    Serial1.print(gps.location.lng(), 6);
    Serial1.print(" | Altitude: ");
    Serial1.print(gps.altitude.meters());
    Serial1.println(" meters");
  } else {
    Serial1.println("GPS data is not valid");
  }
}


void sendSensorData(float temperature, float humidity, float latitude, float longitude, float altitude) {
  // Criar um objeto JSON
  StaticJsonDocument<100> doc;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["latitude"] = latitude;
  doc["longitude"] = longitude;
  doc["altitude"] = altitude; 

  // Serializar o objeto JSON e enviar pela porta serial
  serializeJson(doc, Serial);
  serializeJson(doc, Serial1); // Enviar para Serial1 (UART1)
  Serial.println(); // Adicionar uma nova linha para indicar o fim da mensagem
}

void loop() {
  // Leitura dos dados do sensor DHT11
  float temperature = dht.readTemperature();   // Leitura da temperatura
  float humidity = dht.readHumidity();         // Leitura da umidade

  // Verifica se a leitura do DHT11 foi bem-sucedida
  if (!isnan(temperature) && !isnan(humidity)) {
    // Exibe os dados do sensor DHT11
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C | Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");

    // Leitura e exibição dos dados do módulo GPS
    while (Serial1.available() > 0) {
      if (gps.encode(Serial1.read())) {
        showGPSData();
      }
    }
     // Envia os dados no formato JSON pela porta serial
    sendSensorData(temperature, humidity, gps.location.lat(), gps.location.lng(), gps.altitude.meters());
  
  } else {
    Serial.println("Failed to read from DHT sensor!");
  }


  delay(5000);  // Aguarda 5 segundos antes da próxima leitura
}
