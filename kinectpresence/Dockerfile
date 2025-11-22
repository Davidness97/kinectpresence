FROM hassioaddons/base-ubuntu:latest

# 1. Installazione delle dipendenze di sistema (necessarie per la compilazione)
# jq è necessario per run.sh
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        cmake \
        libusb-1.0-0-dev \
        libturbojpeg \
        libjpeg-dev \
        python3-dev \
        python3-pip \
        cython3 \
        jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Installazione delle librerie Python, compreso il binding del Kinect
RUN pip3 install paho-mqtt numpy \
    && pip3 install --no-cache-dir git+https://github.com/r9y9/pylibfreenect2.git

# 3. Copia i file dell'applicazione
WORKDIR /app
# Copia tutti i file necessari nella cartella root/
COPY kinect_mqtt_bridge.py /app/
COPY run.sh /usr/bin/run.sh
RUN chmod a+x /usr/bin/run.sh

# Punto di ingresso
CMD [ "/usr/bin/run.sh" ]FROM hassioaddons/base-ubuntu:latest

# 1. Installazione delle dipendenze di sistema (necessarie per la compilazione)
# jq è necessario per run.sh
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        cmake \
        libusb-1.0-0-dev \
        libturbojpeg \
        libjpeg-dev \
        python3-dev \
        python3-pip \
        cython3 \
        jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Installazione delle librerie Python, compreso il binding del Kinect
RUN pip3 install paho-mqtt numpy \
    && pip3 install --no-cache-dir git+https://github.com/r9y9/pylibfreenect2.git

# 3. Copia i file dell'applicazione
WORKDIR /app
# Copia tutti i file necessari nella cartella root/
COPY kinect_mqtt_bridge.py /app/
COPY run.sh /usr/bin/run.sh
RUN chmod a+x /usr/bin/run.sh

# Punto di ingresso
CMD [ "/usr/bin/run.sh" ]
