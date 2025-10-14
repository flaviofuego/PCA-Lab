# Dockerfile para compilar y ejecutar el programa PCA en C
# Usa GCC en un contenedor Linux

FROM gcc:latest

# Información del contenedor
LABEL maintainer="PCA Lab"
LABEL description="Entorno para compilar y ejecutar PCA en C"

# Instalar herramientas adicionales si son necesarias
RUN apt-get update && apt-get install -y \
    make \
    cmake \
    liblapack-dev \
    libblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar código fuente
COPY src/ ./src/

# Crear directorio para datos
RUN mkdir -p /app/data

# Comando de compilación
# Se compilará cuando se ejecute el contenedor para permitir cambios en el código
CMD ["sh", "-c", "gcc -o /app/pca_program /app/src/*.c -lm -O2 && /app/pca_program"]
