# Estacao Meteorologica IoT

Este projeto e uma aplicacao IoT para testar a comunicacao de sensores com uma plataforma web usando backend em Python e banco de dados SQLite.

Como nao temos o hardware fisico disponivel agora, construimos uma simulacao por software. O arquivo simulador.py cria dados de temperatura, umidade e pressao. Ele os envia para um broker publico Mosquitto via protocolo MQTT. Isso ajuda a simular o funcionamento das placas e modulos como se fossem reais.

O fluxo do projeto se inicia no simulador gerando os valores e enviando ao servidor MQTT. O script mqtt_reader.py fica ativo aguardando essas informacoes e assim que elas chegam ele realiza um envio via HTTP POST para a API do site. A aplicacao principal feita em Flask recebe as informacoes da leitura e usa o database.py para guarda las no banco de dados. 

O painel de monitoramento web le esses valores salvos no banco de dados e os exibe atraves de tabelas e graficos animados para facilitar a compreensao dos modulos da estacao. 

Para colocar a aplicacao no ar certifique de ter ativado o ambiente virtual em tres terminais separados. No primeiro terminal digite python main.py para rodar o site. No segundo terminal inicie o leitor MQTT rodando python mqtt_reader.py. No terceiro e ultimo terminal ative os envios rodando python simulador.py e os dados comecarao a aparecer assim que voce acessar localhost:5000 no seu navegador padrao.# Sistema de Medicao de Estacao Meteorologica IoT

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
