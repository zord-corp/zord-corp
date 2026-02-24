# Usamos una base de Debian/Ubuntu
FROM python:3.10-slim

# Instalamos dependencias de compilación para PQC
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalamos liboqs (el motor de algoritmos)
RUN git clone https://github.com/open-quantum-safe/liboqs.git /opt/liboqs && \
    mkdir /opt/liboqs/build && cd /opt/liboqs/build && \
    cmake .. && make -j$(nproc) && make install

# Instalamos oqs-provider para OpenSSL 3
RUN git clone https://github.com/open-quantum-safe/oqs-provider.git /opt/oqs-provider && \
    cd /opt/oqs-provider && \
    cmake -S . -B _build && \
    cmake --build _build

# Seteamos las variables de entorno para que OpenSSL encuentre ZORD
ENV OPENSSL_MODULES=/opt/oqs-provider/_build/lib
ENV LD_LIBRARY_PATH=/usr/local/lib

# Copiamos tu código de Zord (incluyendo tu llave privada y archivos .bin)
WORKDIR /app
COPY . .

# Comando para iniciar tu servidor (ajusta según tu archivo principal)
CMD ["python", "app.py"]