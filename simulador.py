import paho.mqtt.client as mqtt
import json
import time
import random

# Configurações do MQTT (mesmas do ESP32/mqtt_reader)
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "estacao/inteli/sensores/mock"

def iniciar_simulador():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        
    print(f"Conectando ao broker {BROKER}...")
    client.connect(BROKER, PORT, 60)
    
    print("Iniciando simulação de sensores (Pressione Ctrl+C para parar)...")
    
    try:
        while True:
            # Gerar dados realistas
            temp = round(random.uniform(15.0, 35.0), 2)
            umid = round(random.uniform(40.0, 80.0), 2)
            pressao = round(random.uniform(1000.0, 1020.0), 2)
            
            dados = {
                "temperatura": temp,
                "umidade": umid,
                "pressao": pressao
            }
            
            payload = json.dumps(dados)
            client.publish(TOPIC, payload)
            
            print(f"Publicado no tópico '{TOPIC}': {payload}")
            
            # Aguarda 5 segundos antes da próxima leitura
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nSimulação encerrada.")
        client.disconnect()

if __name__ == '__main__':
    iniciar_simulador()
