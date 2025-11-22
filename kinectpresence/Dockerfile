FROM ghcr.io/home-assistant/amd64-base:latest

# --- CACHE BREAKER CRITICO ---
# Invalida la cache per garantire che venga eseguita la nuova lista di pacchetti.
RUN echo "Cache invalidation $(date +%s)"

# [Step 2/10] Installa le dipendenze di build e di sistema
# Lista di pacchetti che esistono in Alpine.
RUN apk update && \
    apk add --no-cache build-base cmake libusb-dev mesa-dev pkgconfig python3-dev py3-pip jq git libjpeg-turbo-dev libx11-dev && \
    rm -rf /var/cache/apk/*

# [Step 3/10] Clona, compila e installa libfreenect2
# MODIFICA CRITICA: Forza l'uso del backend CPU per evitare dipendenze OpenGL/GPU non gestibili.
RUN git clone https://github.com/OpenKinect/libfreenect2.git /tmp/libfreenect2 && \
    mkdir -p /tmp/libfreenect2/build && \
    cd /tmp/libfreenect2/build && \
    # Compila con i parametri di default e forza l'installazione in /usr/local
    cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Release -DFREENECT2_BUILD_WITH_CPU=ON -DFREENECT2_WITH_OPENGL=OFF -DFREENECT2_WITH_OPENCL=OFF && \
    make -j$(nproc) && \
    make install && \
    cd / && \
    rm -rf /tmp/libfreenect2

# PASSO 4/10 RIMOSSO (ldconfig fallito)

WORKDIR /app

# [Step 5/10] Copia lo script Python
COPY kinect_mqtt_bridge.py /app/

# [Step 6/10] Installa le dipendenze di base per la compilazione Python
RUN pip3 install --no-cache-dir --break-system-packages numpy cython setuptools paho-mqtt

# [Step 7/10] Installa pylibfreenect2 dalla sorgente. 
# CRITICO: Usa LD_LIBRARY_PATH per il COMPILATORE.
RUN git clone https://github.com/r9y9/pylibfreenect2.git /tmp/pylibfreenect2 && \
    cd /tmp/pylibfreenect2 && \
    PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" \
    LD_LIBRARY_PATH="/usr/local/lib" \
    pip3 install --no-cache-dir --break-system-packages --no-build-isolation . && \
    cd / && \
    rm -rf /tmp/pylibfreenect2

# CONFIGURAZIONE AVVIO CON SCRIPT CRITICA: VARIABILI DI PERCORSO PER IL RUNTIME
# [Step 8/10] Crea e rende eseguibile lo script di avvio. 
# Rimossa LD_DEBUG perché non ha fornito diagnostica.
RUN printf '#!/usr/bin/env bash\n\nset -e\n\n# Messaggio diagnostico di avvio\necho "Inizializzazione script di avvio del container..." 2>&1\n/usr/bin/python3 --version 2>&1\n\n# Aggiunge il percorso della libreria C++ (libfreenect2) per il runtime Python\nexport LD_LIBRARY_PATH="/usr/local/lib":$LD_LIBRARY_PATH\n\n# Aggiunge il percorso di installazione Python\nexport PYTHONPATH="/usr/local/lib/python3.11/site-packages":$PYTHONPATH\n\n# Esegue lo script Python, reindirizzando stderr (errori) a stdout (log)\nexec /usr/bin/python3 /app/kinect_mqtt_bridge.py 2>&1\n' > /run.sh
RUN chmod +x /run.sh

# [Step 9/10] L'istruzione CMD esegue lo script di avvio.
CMD [ "/run.sh" ]
