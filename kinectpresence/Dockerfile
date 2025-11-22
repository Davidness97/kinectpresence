ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest 
FROM $BUILD_FROM

# 1. Installazione delle dipendenze di sistema (necessarie per la compilazione e runtime)
RUN apk update \
    && apk add --no-cache build-base cmake libusb-dev mesa-dev pkgconfig python3-dev py3-pip jq git libjpeg-turbo-dev libx11-dev \
    && rm -rf /var/cache/apk/*

RUN git clone https://github.com/OpenKinect/libfreenect2.git /tmp/libfreenect2 \
    && mkdir -p /tmp/libfreenect2/build \
    && cd /tmp/libfreenect2/build \
    && cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local \
    && make -j$(nproc) \
    && make install \
    && cd / \
    && rm -rf /tmp/libfreenect2

# 3. Definizione dell'ambiente Python e installazione di Mqtt
WORKDIR /app

# 2. Definizione dell'ambiente Python e installazione di Mqtt
WORKDIR /app
COPY kinect_mqtt_bridge.py /app/

RUN PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" 

LD_LIBRARY_PATH="/usr/local/lib"

# 1. Installazione di NumPy e dipendenze di build (per risolvere il ModuleNotFoundError)
RUN pip3 install \
    --no-cache-dir \
    --break-system-packages \
    numpy \
    cython \
    setuptools

# 2. Installazione delle dipendenze principali (Ora l'ambiente di build è pronto)
RUN pip3 install \
    --no-cache-dir \
    --break-system-packages \
    --no-build-isolation \
    paho-mqtt \
    pylibfreenect2

# 3. Copia del run.sh e impostazione dei permessi
# Nota: run.sh viene copiato in /usr/bin e non in /app
COPY run.sh /usr/bin/run.sh
RUN chmod a+x /usr/bin/run.sh

# 4. ENTRYPOINT: L'esecuzione parte da qui
CMD [ "/usr/bin/run.sh" ]















