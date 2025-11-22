FROM ghcr.io/home-assistant/amd64-base:latest

# [Step 2/10] Installa le dipendenze di build e di sistema
RUN apk update && \
    apk add --no-cache build-base cmake libusb-dev mesa-dev pkgconfig python3-dev py3-pip jq git libjpeg-turbo-dev libx11-dev && \
    rm -rf /var/cache/apk/*

# [Step 3/10] Clona, compila e installa libfreenect2
# Questo crea la libreria C++ in /usr/local/
RUN git clone https://github.com/OpenKinect/libfreenect2.git /tmp/libfreenect2 && \
    mkdir -p /tmp/libfreenect2/build && \
    cd /tmp/libfreenect2/build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local && \
    make -j$(nproc) && \
    make install && \
    cd / && \
    rm -rf /tmp/libfreenect2

WORKDIR /app

# [Step 6/10] Copia lo script Python
COPY kinect_mqtt_bridge.py /app/

# [Step 7/10] Installa le dipendenze di base per la compilazione Python
RUN pip3 install --no-cache-dir --break-system-packages numpy cython setuptools

# [Step 8/10 - CORRETTO] Installa paho-mqtt e pylibfreenect2
# Imposta PKG_CONFIG_PATH e LD_LIBRARY_PATH per consentire a pylibfreenect2 
# di trovare la libreria libfreenect2 installata in /usr/local/.
RUN PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" LD_LIBRARY_PATH="/usr/local/lib" pip3 install --no-cache-dir --break-system-packages --no-build-isolation paho-mqtt pylibfreenect2

# Comando di esecuzione predefinito (presupponendo l'uso del file kinect_mqtt_bridge.py)
CMD [ "python3", "kinect_mqtt_bridge.py" ]
