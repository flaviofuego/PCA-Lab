# Makefile para el laboratorio de PCA
# Sistema: Linux/Unix
# Compilador: GCC via Docker

# Variables
DOCKER_IMAGE = pca-lab-gcc
DOCKER_CONTAINER = pca-lab-container
DATA_DIR = data
PYTHON_DIR = python
SRC_DIR = src
REPORT_DIR = report
CURRENT_DIR = $(shell pwd)

# Parámetros de datos (configurables)
SAMPLES ?= 20
FEATURES ?= 5
N_COMPONENTS ?= 2
TYPE ?= classification
CLUSTERS ?= 3
TIMESTAMP ?= true

# Colores para output (Linux)
BLUE = \033[94m
GREEN = \033[92m
RESET = \033[0m

.PHONY: all help setup generate-data build run validate clean clean-all

help:
	@echo "======================================"
	@echo "  Makefile - Laboratorio PCA en C"
	@echo "======================================"
	@echo ""
	@echo "Targets disponibles:"
	@echo "  make setup          - Instala dependencias de Python"
	@echo "  make generate-data  - Genera datos sintéticos"
	@echo "  make build          - Construye la imagen Docker con GCC"
	@echo "  make run            - Ejecuta el algoritmo PCA en C"
	@echo "  make validate       - Valida resultados con sklearn"
	@echo "  make clean          - Limpia archivos generados"
	@echo "  make clean-all      - Limpia todo incluyendo Docker"
	@echo "  make all-steps      - Ejecuta todos los pasos en orden"
	@echo ""
	@echo "Parámetros configurables:"
	@echo "  SAMPLES=<num>       - Número de muestras (default: 20)"
	@echo "  FEATURES=<num>      - Número de dimensiones (default: 5)"
	@echo "  N_COMPONENTS=<num>  - Número de componentes principales (default: 2)"
	@echo "  TYPE=<tipo>         - Tipo de datos: classification o blobs (default: classification)"
	@echo "  CLUSTERS=<num>      - Número de clusters para tipo blobs (default: 3)"
	@echo "  TIMESTAMP=<bool>    - Versionar archivos con timestamp: true o false (default: true)"
	@echo ""
	@echo "Ejemplos de uso:"
	@echo "  make all-steps SAMPLES=1000 FEATURES=10"
	@echo "  make all-steps SAMPLES=500 FEATURES=8 TYPE=blobs"
	@echo "  make all-steps SAMPLES=1000 FEATURES=10 TIMESTAMP=false  # Sin versionado"
	@echo "  make all-steps SAMPLES=1000 FEATURES=10 N_COMPONENTS=3   # 3 componentes principales"
	@echo "  make all-steps SAMPLES=1000 FEATURES=10 TYPE=blobs CLUSTERS=5  # 5 clusters"
	@echo "  make generate-data SAMPLES=2000 FEATURES=15 TYPE=classification"
	@echo ""

# Instalar dependencias de Python
setup:
	@echo "Instalando dependencias de Python..."
	python -m pip install --upgrade pip
	pip install -r $(PYTHON_DIR)/requirements.txt
	@echo "Dependencias instaladas correctamente"

# Generar datos sintéticos
generate-data:
	@echo "======================================"
	@echo "  Generando datos sintéticos..."
	@echo "  Tipo: $(TYPE)"
ifeq ($(TYPE),blobs)
	@echo "  Clusters: $(CLUSTERS)"
endif
	@echo "  Timestamp: $(TIMESTAMP)"
	@echo "======================================"
ifeq ($(TIMESTAMP),true)
	python $(PYTHON_DIR)/generate_data.py --samples $(SAMPLES) --features $(FEATURES) --type $(TYPE) --clusters $(CLUSTERS) --timestamp
else
	python $(PYTHON_DIR)/generate_data.py --samples $(SAMPLES) --features $(FEATURES) --type $(TYPE) --clusters $(CLUSTERS)
endif
	@echo ""
	@echo "Datos generados exitosamente"

# Construir imagen Docker
build:
	@echo "======================================"
	@echo "  Construyendo imagen Docker..."
	@echo "======================================"
	docker build -t $(DOCKER_IMAGE) .
	@echo ""
	@echo "Imagen Docker construida: $(DOCKER_IMAGE)"

# Ejecutar PCA en C usando Docker
run:
	@echo "======================================"
	@echo "  Ejecutando PCA en C (Docker)..."
	@echo "  Timestamp: $(TIMESTAMP)"
	@echo "  N_Components: $(N_COMPONENTS)"
	@echo "======================================"
	@echo "Montando volumenes y ejecutando contenedor..."
ifeq ($(TIMESTAMP),true)
	$(eval CURRENT_TIMESTAMP := $(shell date +%Y%m%d_%H%M%S))
	docker run --rm -e TIMESTAMP="$(CURRENT_TIMESTAMP)" -e N_COMPONENTS="$(N_COMPONENTS)" -v "$(CURRENT_DIR)/$(DATA_DIR):/app/data" -v "$(CURRENT_DIR)/$(SRC_DIR):/app/src" $(DOCKER_IMAGE)
else
	docker run --rm -e N_COMPONENTS="$(N_COMPONENTS)" -v "$(CURRENT_DIR)/$(DATA_DIR):/app/data" -v "$(CURRENT_DIR)/$(SRC_DIR):/app/src" $(DOCKER_IMAGE)
endif
	@echo ""
	@echo "======================================"
	@echo "  PCA ejecutado exitosamente!"
	@echo "======================================"
	@echo "Resultados guardados en: $(DATA_DIR)/output_data.csv"
ifeq ($(TIMESTAMP),true)
	@echo "Archivo versionado: $(DATA_DIR)/output_data_$(CURRENT_TIMESTAMP).csv"
endif
	@echo ""

# Compilar localmente (sin Docker) - requiere GCC instalado
compile-local:
	@echo "======================================"
	@echo "  Compilando PCA localmente..."
	@echo "======================================"
	gcc -o pca_program $(SRC_DIR)/main.c $(SRC_DIR)/pca.c -lm -O2 -Wall
	@echo "Compilacion exitosa: pca_program"

# Ejecutar localmente (despues de compile-local)
run-local:
	@echo "======================================"
	@echo "  Ejecutando PCA localmente..."
	@echo "  N_Components: $(N_COMPONENTS)"
	@echo "======================================"
	./pca_program $(DATA_DIR)/input_data.csv $(DATA_DIR)/output_data.csv $(N_COMPONENTS)

# Validar resultados
validate:
	@echo "======================================"
	@echo "  Validando resultados..."
	@echo "  Timestamp: $(TIMESTAMP)"
	@echo "======================================"
	@mkdir -p $(REPORT_DIR)
	@mkdir -p $(REPORT_DIR)/comparison_plots
ifeq ($(TIMESTAMP),true)
	cd $(PYTHON_DIR) && python validate_pca.py --timestamp
else
	cd $(PYTHON_DIR) && python validate_pca.py
endif
	@echo ""
	@echo "Validacion completada. Ver resultados en $(REPORT_DIR)/"

# Limpiar archivos generados
clean:
	@echo "Limpiando archivos generados..."
	@rm -f $(DATA_DIR)/*.csv
	@rm -f $(DATA_DIR)/*.txt
	@rm -f $(REPORT_DIR)/*.png
	@rm -f $(REPORT_DIR)/*.txt
	@rm -f $(REPORT_DIR)/comparison_plots/*.png
	@rm -f $(SRC_DIR)/*.o
	@rm -f $(SRC_DIR)/*.exe
	@rm -f $(SRC_DIR)/pca_program
	@echo "Archivos limpiados"

# Limpiar todo incluyendo Docker
clean-all: clean
	@echo "Eliminando contenedores e imagenes Docker..."
	-docker rm -f $(DOCKER_CONTAINER) 2>/dev/null || true
	-docker rmi -f $(DOCKER_IMAGE) 2>/dev/null || true
	@echo "Limpieza completa realizada"

# Ejecutar todos los pasos
all-steps: setup generate-data build run validate
	@echo ""
	@echo "======================================"
	@echo "  Proceso completado exitosamente"
	@echo "======================================"
	@echo ""
	@echo "Revisa los resultados en:"
	@echo "  - Datos de entrada: $(DATA_DIR)/input_data.csv"
	@echo "  - Datos de salida: $(DATA_DIR)/output_data.csv"
	@echo "  - Graficas: $(REPORT_DIR)/comparison_plots/"
	@echo "  - Reporte: $(REPORT_DIR)/comparison_report.txt"

all: generate-data build run validate
	@echo ""
	@echo "======================================"
	@echo "  Proceso completado exitosamente"
	@echo "======================================"
	@echo ""
	@echo "Revisa los resultados en:"
	@echo "  - Datos de entrada: $(DATA_DIR)/input_data.csv"
	@echo "  - Datos de salida: $(DATA_DIR)/output_data.csv"
	@echo "  - Graficas: $(REPORT_DIR)/comparison_plots/"
	@echo "  - Reporte: $(REPORT_DIR)/comparison_report.txt"