#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "NOME_DA_SUA_WIFI";
const char* password = "SENHA_DA_WIFI";

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
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    String clientId = "ESP32Client-";
    clientId += String(random(0, 1000));
    
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
  
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;

    float mock_temp = 15.0 + random(0, 2000) / 100.0;
    float mock_umid = 40.0 + random(0, 4000) / 100.0;
    float mock_pressao = 1000.0 + random(0, 2000) / 100.0;

    String jsonPayload = "{";
    jsonPayload += "\"temperatura\": " + String(mock_temp, 2) + ", ";
    jsonPayload += "\"umidade\": " + String(mock_umid, 2) + ", ";
    jsonPayload += "\"pressao\": " + String(mock_pressao, 2);
    jsonPayload += "}";

    Serial.print("Enviando via MQTT no tópico '");
    Serial.print(mqtt_topic);
    Serial.println("':");
    Serial.println(jsonPayload);
    
    client.publish(mqtt_topic, jsonPayload.c_str());
  }
}
