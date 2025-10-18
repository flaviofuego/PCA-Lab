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
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar código fuente
COPY src/ ./src/

# Crear directorio para datos
RUN mkdir -p /app/data

# Comando de compilación y ejecución
# Compila los archivos C y ejecuta el programa PCA
CMD ["sh", "-c", "echo '========================================' && \
     echo 'Compiling PCA program...' && \
     echo '========================================' && \
     gcc -o /app/pca_program /app/src/main.c /app/src/pca.c -lm -O2 -Wall && \
     echo 'Compilation successful!' && \
     echo '' && \
     if [ -n \"$TIMESTAMP\" ]; then \
       /app/pca_program /app/data/input_data.csv /app/data/output_data.csv 2 \"$TIMESTAMP\"; \
     else \
       /app/pca_program /app/data/input_data.csv /app/data/output_data.csv 2; \
     fi"]
