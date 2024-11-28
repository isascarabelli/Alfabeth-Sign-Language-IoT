// mqttServer.js
const mqtt = require('mqtt');
const express = require('express');
const request = require('request');
const cors = require('cors');
const http = require('http');

const app = express();
app.use(cors());

// Conecta ao Mosquitto usando o protocolo MQTT/TCP
const client = mqtt.connect('mqtt://test.mosquitto.org');

// Variável para armazenar a última mensagem recebida
let lastMessage1 = '';
let lastMessage2 = '';

client.on('connect', () => {
  console.log('Conectado ao Mosquitto via MQTT/TCP');
  
  // Assinatura de um tópico
  client.subscribe('signalLang/topic/sending1', (err) => {
    if (!err) {
      console.log('Inscrito no tópico 1');
    }
  });

  client.subscribe('signalLang/topic/sending2', (err) => {
    if (!err) {
      console.log('Inscrito no tópico 2');
    }
  });
});

// Armazena a mensagem recebida
client.on('message', (topic, message) => {
  console.log(`Mensagem recebida no tópico ${topic}:`, message.toString());

  if (topic == "signalLang/topic/sending1") {
    lastMessage1 = message.toString();
  } else {
    lastMessage2 = message.toString();
  }
});

// API para enviar a última mensagem ao cliente React
app.get('/mqtt-message', (req, res) => {
  res.json({ 
    message1: lastMessage1,
    message2: lastMessage2
   });
});

// Inicializa o servidor HTTP
const server = http.createServer(app);
const PORT = 5000;
server.listen(PORT, () => {
  console.log(`Servidor HTTP rodando na porta ${PORT}`);
});
