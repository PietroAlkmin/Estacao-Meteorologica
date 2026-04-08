# Sistema de Medicao de Estacao Meteorologica IoT

## 1. Apresentacao
Este e um projeto desenvolvido para a atividade ponderada do Modulo 5 (Engenharia da Computacao).
Consiste em um sistema completo simulando uma estacao meteorologica.

## 2. Decisoes de Arquitetura e Justificativas

De acordo com as instucoes do PDF (Item 5.2):
> "Caso os sensores físicos não estejam disponíveis, implemente um modo de simulação no próprio Arduino (ou em Python) que gere valores aleatórios realistas. Documente essa decisão."

**Decisões tomadas:**
1. **Simulação por Software (Sem hardware físico):** Criamos o script `simulador.py` na linguagem Python. Ele gera valores perfeitamente enquadrados em amostras climáticas reais para Temperatura (15ºC~35ºC), Umidade (40%~80%) e Pressão (1000~1020 hPa). 
2. **Substituição da Porta Serial por MQTT:** Em vez de conectar via cabo Serial `COM`, estamos enviando os dados JSON para o broker público `test.mosquitto.org` (Tópico: `estacao/inteli/sensores/mock`). 
3. **Escuta do Brokder (Ponte MQTT->Flask):** O script `mqtt_reader.py` assina o tópico no broker, capta as medições assim que chegam, os decodifica e realiza um POST na rota `/leituras` da API Flask localmente (atuando como a camada "Serial" proposta na arquitetura inicial, só que via rede).

## 3. Requisitos e Instalação

```bash
# 1. Ativar o ambiente virtual e instalar dependências
python -m venv venv
venv\Scripts\activate   # Windows
pip install flask pyserial paho-mqtt requests

# 2. Inicialize o Banco SQLite (main.py já invoca essa função)
```

## 4. Como Executar (3 Terminais Simultâneos)

Para o fluxo todo funcionar, você precisará de três instâncias de terminal abrindo:

**Terminal 1: Servidor Flask API**
```bash
python main.py
```
*(Inicia a API REST, Dashboard na porta 5000: http://localhost:5000/)*

**Terminal 2: Escuta de mensagens (Ponte MQTT para HTTP POST)**
```bash
python mqtt_reader.py
```
*(Monitora a Nuvem e repassa tudo que chegar em `estacao/inteli/sensores/mock` por POST pro banco nas rotas de Flask)*.

**Terminal 3: Simulador do Hardware IoT**
```bash
python simulador.py
```
*(A cada 5 segundos, publica dados aleatórios no Tópico do MQTT test.mosquitto.org, simulando os sensores de um ESP32. Esse terminal faz o papel do dispositivo real conectado ao Ardiuno).*

## 5. Rotas da API

- `GET /` — Painel principal em Web de resumo e gráfico Chart.js (Real-Time update de 10s).
- `GET /leituras` — Tabela completa (Web).
- `POST /leituras` — Rota de consumo para a ponte de MQTT onde os mocks entram no SQLite.
- `GET /leituras/<id>` — Detalhe do dado.
- `PUT/POST /leituras/<id>/atualizar` - Modifica dados pontuais (Editar na Web).
- `DELETE/POST /leituras/<id>/deletar` - Exclui o ID correspondente da Tabela (Limpar sujeiras).
- `GET /api/estatisticas` - Consolidados Json de AVG, MAX, MIN para o período.
