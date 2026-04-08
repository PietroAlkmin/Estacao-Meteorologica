#include <WiFi.h>
#include <PubSubClient.h>

// ======= CONFIGURAÇÕES DA REDE WIFI =========
const char* ssid = "NOME_DA_SUA_WIFI";
const char* password = "SENHA_DA_WIFI";

// ======= CONFIGURAÇÕES DO MQTT ==============
const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 1883;
const char* mqtt_topic = "estacao/inteli/sensores/mock";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando à rede: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi Conectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop até conectar
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    // Cria um ID de cliente aleatório
    String clientId = "ESP32Client-";
    clientId += String(random(0, 1000));
    
    // Tenta conectar
    if (client.connect(clientId.c_str())) {
      Serial.println("conectado ao broker MQTT!");
    } else {
      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(0));

  setup_wifi();
  
  // Configura o servidor do broker
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Enviar a cada 5 segundos
  unsigned long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;

    // GERANDO DADOS MOCADOS
    // Simulando dht.readTemperature() / dht.readHumidity()
    // Temperatura entre 15.0 e 35.0
    float mock_temp = 15.0 + random(0, 2000) / 100.0;
    // Umidade entre 40.0 e 80.0
    float mock_umid = 40.0 + random(0, 4000) / 100.0;
    // Pressão simulada em hPa entre 1000 e 1020
    float mock_pressao = 1000.0 + random(0, 2000) / 100.0;

    // Construção do payload JSON manualmente para não precisar da biblioteca ArduinoJson
    String jsonPayload = "{";
    jsonPayload += "\"temperatura\": " + String(mock_temp, 2) + ", ";
    jsonPayload += "\"umidade\": " + String(mock_umid, 2) + ", ";
    jsonPayload += "\"pressao\": " + String(mock_pressao, 2);
    jsonPayload += "}";

    // Publicando no broker
    Serial.print("Enviando via MQTT no tópico '");
    Serial.print(mqtt_topic);
    Serial.println("':");
    Serial.println(jsonPayload);
    
    // Convertendo para array de char e mandando via PubSubClient
    client.publish(mqtt_topic, jsonPayload.c_str());
  }
}
