FROM ghcr.io/home-assistant/amd64-base:latest

# [Step 2/11] Installa le dipendenze di build e di sistema
RUN apk update && \
    apk add --no-cache build-base cmake libusb-dev mesa-dev pkgconfig python3-dev py3-pip jq git libjpeg-turbo-dev libx11-dev && \
    rm -rf /var/cache/apk/*

# [Step 3/11] Clona, compila e installa libfreenect2
# Questo crea la libreria C++ in /usr/local/
RUN git clone https://github.com/OpenKinect/libfreenect2.git /tmp/libfreenect2 && \
    mkdir -p /tmp/libfreenect2/build && \
    cd /tmp/libfreenect2/build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local && \
    make -j$(nproc) && \
    make install && \
    cd / && \
    rm -rf /tmp/libfreenect2

# [NUOVO STEP 4/11] Aggiunge il percorso della libreria C++ tramite file di configurazione e aggiorna la cache.
# Questo è il metodo standard e robusto per Alpine Linux.
RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/libfreenect2.conf && ldconfig

WORKDIR /app

# [Step 6/11] Copia lo script Python
COPY kinect_mqtt_bridge.py /app/

# [Step 7/11] Installa le dipendenze di base per la compilazione Python
RUN pip3 install --no-cache-dir --break-system-packages numpy cython setuptools paho-mqtt

# [Step 8/11] Installa pylibfreenect2 dalla sorgente (richiede il percorso corretto solo per il build)
RUN git clone https://github.com/r9y9/pylibfreenect2.git /tmp/pylibfreenect2 && \
    cd /tmp/pylibfreenect2 && \
    PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" \
    LD_LIBRARY_PATH="/usr/local/lib" \
    pip3 install --no-cache-dir --break-system-packages --no-build-isolation . && \
    cd / && \
    rm -rf /tmp/pylibfreenect2

# CONFIGURAZIONE AVVIO CON SCRIPT CORRETTO
# Manteniamo l'export LD_LIBRARY_PATH nello script di avvio per massima sicurezza.

# [Step 9/11] Crea e rende eseguibile lo script di avvio
RUN printf '#!/usr/bin/env bash\n\nset -e\n\n# Aggiunge il percorso della libreria C++ (libfreenect2) per il runtime Python\nexport LD_LIBRARY_PATH="/usr/local/lib":$LD_LIBRARY_PATH\n\n# Esegue lo script Python e lo mantiene come PID 1\nexec /usr/bin/python3 /app/kinect_mqtt_bridge.py\n' > /run.sh
RUN chmod +x /run.sh

# [Step 10/11] L'istruzione CMD esegue lo script di avvio.
CMD [ "/run.sh" ]
