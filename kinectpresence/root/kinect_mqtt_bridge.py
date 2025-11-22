import paho.mqtt.client as mqtt
import numpy as np
import time
from pylibfreenect2 import Freenect2, SyncMultiFrameListener, FrameType
import os # ESSENZIALE per l'Add-on

# --- PARAMETRI DI CONFIGURAZIONE (LEGGE DALLE VARIABILI D'AMBIENTE) ---
# I valori sono letti dalle variabili d'ambiente iniettate da run.sh
MQTT_BROKER = os.environ.get('MQTT_BROKER', 'core-mqtt') 
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))

# Le credenziali vengono lette da run.sh
MQTT_USER = os.environ.get('MQTT_USER', '') 
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', '')

# I topic sono letti da run.sh o definiti come costanti
TOPIC_PRESENZA = os.environ.get('TOPIC_PRESENZA', "kinect/sala/presenza")
TOPIC_DISTANZA = "kinect/sala/distanza_minima"
TOPIC_CONTEGGIO = "kinect/sala/conteggio_persone"

# Parametri Kinect letti dalla configurazione dell'Add-on
UMIDITA_PROFONDITA = float(os.environ.get('UMIDITA_PROFONDITA_MM', 3800.0))
SOGLIA_PIXEL = int(os.environ.get('SOGLIA_PIXEL', 5000))
# ------------------------------------

# Inizializzazione MQTT
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    # Il codice 0 significa connessione riuscita!
    print(f"Connesso al broker MQTT con codice {rc}")
    
    # Pubblica subito lo stato OFF per forzare l'entità HA a uscire da "sconosciuto"
    client.publish(TOPIC_PRESENZA, "OFF", retain=True) 
    print("Pubblicato stato iniziale OFF.")

client.on_connect = on_connect

# Configurazione credenziali per risolvere l'errore "not authorised"
if MQTT_USER and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"Errore nella connessione MQTT: {e}")
    
# Inizializzazione Kinect
try:
    fn = Freenect2(pipeline="cpu") 
    device = fn.openDefaultDevice()
    
    if device is None:
        print("Nessun dispositivo Kinect v2 trovato o impossibile aprirlo.")
        exit(1)

    listener = SyncMultiFrameListener(FrameType.Color | FrameType.Ir | FrameType.Depth)
    device.setIrAndDepthFrameListener(listener)
    device.setColorFrameListener(listener)
    
    device.start() 
    print("Kinect V2 avviato...")

except Exception as e:
    print(f"Errore nell'avvio del Kinect: {e}. Controllare passthrough USB e driver.")
    exit(1)

stato_precedente = False 

try:
    while True:
        # 1. Acquisisci il frame dal Kinect
        frames = listener.waitForNewFrame() 
        depth_frame = frames["depth"]
        depth_data = depth_frame.asarray(np.float32) 

        # 2. Logica di Rilevamento e Misurazione
        
        # Conta i pixel che rientrano nella soglia di profondità
        pixel_vicini = np.sum(np.logical_and(depth_data > 1.0, depth_data < UMIDITA_PROFONDITA))

        # Calcola la distanza minima tra gli oggetti validi
        valid_depths = depth_data[(depth_data > 1.0) & (depth_data < UMIDITA_PROFONDITA)]
        min_distance = np.min(valid_depths) if valid_depths.size > 0 else 0
        
        presenza_attuale = pixel_vicini > SOGLIA_PIXEL
        
        # 3. Pubblicazione MQTT
        
        # Pubblica DISTANZA MINIMA (in millimetri)
        client.publish(TOPIC_DISTANZA, str(int(min_distance)), retain=False)

        # Pubblica CONTEGGIO PERSONE (semplificato a 0 o 1)
        conteggio = "1" if presenza_attuale else "0"
        client.publish(TOPIC_CONTEGGIO, conteggio, retain=False)
        
        # Pubblica PRESENZA (solo se lo stato è cambiato)
        if presenza_attuale != stato_precedente:
            payload = "ON" if presenza_attuale else "OFF"
            client.publish(TOPIC_PRESENZA, payload, retain=True)
            print(f"Presenza: {payload} | Distanza Min: {int(min_distance)} mm | Pixel Vicini: {pixel_vicini}")
            stato_precedente = presenza_attuale

        # 4. Cleanup e Loop
        listener.release(frames) 
        time.sleep(0.5) 

except KeyboardInterrupt:
    print("\nChiusura script...")
finally:
    # Pulizia
    device.stop()
    device.close()
    client.loop_stop()
    client.disconnect()
    print("Pulizia completata.")
