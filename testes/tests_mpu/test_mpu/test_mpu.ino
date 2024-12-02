#include <Wire.h>
#include <MPU6050.h>
#include <WiFi.h>
#include <HTTPClient.h>

MPU6050 mpu;

// Defina as credenciais do Wi-Fi
const char* ssid = "CaravanaNet";    // Coloque o nome da sua rede Wi-Fi
const char* password = "caravana2024";  // Coloque a senha da sua rede Wi-Fi
String serverName = "http://192.168.43.251:5000/update"; // URL do seu servidor

/*long previousMillis = 0;
const long interval = 50; // Intervalo para leitura dos dados do sensor*/

void setup() {
  Wire.begin();

  //Serial.begin(9600);
  // Conectar ao Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(80);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado!");

  // Iniciar o MPU6050
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 falhou!");
    while (1);
  }
  Serial.println("MPU6050 conectado com sucesso!");
}

void loop() {
  /*long currentMillis = millis();
  
  // Realizar leituras a cada 'interval' milissegundos
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;*/
    
    // Ler os dados de aceleração e giroscópio
  int16_t ax, ay, az;
  int16_t gx, gy, gz;
    
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    // Mapeamento dos dados do acelerômetro e giroscópio para valores compreensíveis
  float accX = (float)ax / 16384.0;
  float accY = (float)ay / 16384.0;
  float accZ = (float)az / 16384.0;

  float gyroX = (float)gx / 131.0;
  float gyroY = (float)gy / 131.0;
  float gyroZ = (float)gz / 131.0;

    // Enviar os dados via Serial ou HTTP (ajustar conforme necessidade)
    /*Serial.print("Acelerômetro -> X: "); Serial.print(accX);
    Serial.print(" Y: "); Serial.print(accY);
    Serial.print(" Z: "); Serial.print(accZ);
    Serial.println();

    Serial.print("Giroscópio -> X: "); Serial.print(gyroX);
    Serial.print(" Y: "); Serial.print(gyroY);
    Serial.print(" Z: "); Serial.print(gyroZ);
    Serial.println();*/
// Verifica se está conectado ao Wi-Fi
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Iniciar a requisição HTTP
    //http.begin(serverName.c_str()); 
    http.begin(serverName);

    // Adicionar cabeçalho HTTP para URL encoded
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    // Criar string com os dados no formato 'key=value&key=value'
    String httpRequestData = "accX=" + String(accX, 4) + "&accY=" + String(accY, 4) +
                             "&accZ=" + String(accZ, 4) + "&gyroX=" + String(gyroX, 4) +
                             "&gyroY=" + String(gyroY, 4) + "&gyroZ=" + String(gyroZ, 4);

    // Enviar a requisição POST com a string formatada
    int httpResponseCode = http.POST(httpRequestData);

    // Verificar o código de resposta
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Resposta do servidor: " + response);
    } else {
      Serial.println("Erro na requisição HTTP: " + String(httpResponseCode));
    }

    // Fechar a conexão HTTP
    http.end();
  } else {
    Serial.println("Erro: não conectado ao Wi-Fi.");
  }

  // Intervalo de leitura (ajustável conforme necessário)
  delay(80);
}
  
  

