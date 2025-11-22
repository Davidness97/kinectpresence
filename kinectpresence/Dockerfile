ARG BUILD_FROM
FROM $BUILD_FROM

# 1. Installazione delle dipendenze di sistema (necessarie per la compilazione e runtime)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        # Dipendenze per LibFreenect2 e Python
        build-essential \
        cmake \
        libusb-1.0-0-dev \
        libgl-dev \
        pkg-config \
        python3-dev \
        python3-pip \
        # Tool di basso livello per USB e file
        jq \
        git \
    && rm -rf /var/lib/apt/lists/*

# 2. Definizione dell'ambiente Python e installazione di Mqtt
WORKDIR /app
COPY kinect_mqtt_bridge.py /app/

# Installazione delle dipendenze Python: paho-mqtt per la comunicazione e il compilatore del Kinect
RUN pip3 install --no-cache-dir \
    paho-mqtt \
    # Compilatore e bridge per il Kinect v2
    pylibfreenect2

# 3. Copia del run.sh e impostazione dei permessi
# Nota: run.sh viene copiato in /usr/bin e non in /app
COPY run.sh /usr/bin/run.sh
RUN chmod a+x /usr/bin/run.sh

# 4. ENTRYPOINT: L'esecuzione parte da qui
CMD [ "/usr/bin/run.sh" ]

