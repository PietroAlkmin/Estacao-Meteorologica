import json
import time
import requests
import paho.mqtt.client as mqtt

# Configurações do MQTT
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "estacao/inteli/sensores/mock"  # Você pode alterar esse tópico caso precise

# URL da nossa API Flask
API_URL = 'http://localhost:5000/leituras'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Conectado com sucesso ao broker MQTT: {BROKER}:{PORT}")
        client.subscribe(TOPIC)
        print(f"Inscrito no tópico: {TOPIC}")
    else:
        print(f"Falha ao conectar. Código de resultado: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    print(f"\nMensagem recebida no tópico {msg.topic}: {payload}")
    
    try:
        dados = json.loads(payload)
        
        # Envia os dados para a API Flask via POST
        print("Enviando para a API Flask...")
        response = requests.post(API_URL, json=dados)
        
        if response.status_code == 201:
            print(f"Dados salvos com sucesso! ID no banco: {response.json().get('id')}")
        else:
            print(f"Erro retornado pela API: {response.status_code} - {response.text}")
            
    except json.JSONDecodeError:
        print("Formato inválido! O payload não pôde ser lido como JSON.")
    except requests.exceptions.RequestException as e:
        print(f"Não foi possível conectar com a API Flask: {e}")
        print("A API no Flask (app.py/main.py) está rodando na porta 5000?")

def iniciar_mqtt():
    # Usando a versão correta da API do Paho MQTT para evitar mensagens estranhas no terminal
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        print(f"Tentando conexão com o broker {BROKER}...")
        client.connect(BROKER, PORT, 60)
        # Mantém a conexão ativa "escutando" as mensagens
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nEncerrando leitura do MQTT.")
        client.disconnect()

if __name__ == '__main__':
    iniciar_mqtt()
