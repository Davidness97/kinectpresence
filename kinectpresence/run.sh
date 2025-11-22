#!/usr/bin/env bash
set -e

# Legge i valori di configurazione inseriti dall'utente in Home Assistant (dal file /data/options.json)
MQTT_BROKER=$(jq -r '.mqtt_broker' /data/options.json)
MQTT_USER=$(jq -r '.mqtt_user' /data/options.json)
MQTT_PASSWORD=$(jq -r '.mqtt_password' /data/options.json)
TOPIC_PRESENZA=$(jq -r '.topic_presenza' /data/options.json)
SOGLIA_PIXEL=$(jq -r '.soglia_pixel' /data/options.json)
UMIDITA_PROFONDITA_MM=$(jq -r '.umidita_profondita_mm' /data/options.json)

# Esporta le configurazioni come variabili d'ambiente.
# Il tuo script Python (kinect_mqtt_bridge.py) leggerà questi valori tramite os.environ.get()
export MQTT_BROKER=$MQTT_BROKER
export MQTT_USER=$MQTT_USER
export MQTT_PASSWORD=$MQTT_PASSWORD
export TOPIC_PRESENZA=$TOPIC_PRESENZA
export SOGLIA_PIXEL=$SOGLIA_PIXEL
export UMIDITA_PROFONDITA_MM=$UMIDITA_PROFONDITA_MM

echo "Avvio del bridge Kinect MQTT..."
# Avvia il tuo script Python
exec python3 /app/kinect_mqtt_bridge.py