# Makefile para el laboratorio de PCA
# Sistema: Windows (PowerShell)
# Compilador: GCC via Docker

# Variables
DOCKER_IMAGE = pca-lab-gcc
DOCKER_CONTAINER = pca-lab-container
DATA_DIR = data
PYTHON_DIR = python
SRC_DIR = src
REPORT_DIR = report
CURRENT_DIR = $(shell cd)

# Parámetros de datos (configurables)
SAMPLES ?= 1000
FEATURES ?= 15
N_COMPONENTS ?= 2

# Colores para output (Windows PowerShell)
BLUE = [94m
GREEN = [92m
RESET = [0m

.PHONY: all help setup generate-data build run validate clean clean-all

# Target por defecto
all: help

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
	@echo "======================================"
	@if not exist "$(DATA_DIR)" mkdir "$(DATA_DIR)"
	python $(PYTHON_DIR)/generate_data.py --samples $(SAMPLES) --features $(FEATURES)
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
	@echo "======================================"
	@if not exist "$(DATA_DIR)" mkdir "$(DATA_DIR)"
	@echo "Montando volumenes y ejecutando contenedor..."
	docker run --rm -v "$(CURRENT_DIR)/$(DATA_DIR):/app/data" -v "$(CURRENT_DIR)/$(SRC_DIR):/app/src" $(DOCKER_IMAGE)
	@echo ""
	@echo "======================================"
	@echo "  PCA ejecutado exitosamente!"
	@echo "======================================"
	@echo "Resultados guardados en: $(DATA_DIR)/output_data.csv"
	@echo ""

# Compilar localmente (sin Docker) - requiere GCC instalado
compile-local:
	@echo "======================================"
	@echo "  Compilando PCA localmente..."
	@echo "======================================"
	gcc -o pca_program $(SRC_DIR)/main.c $(SRC_DIR)/pca.c -lm -O2 -Wall
	@echo "Compilacion exitosa: pca_program.exe"

# Ejecutar localmente (despues de compile-local)
run-local:
	@echo "======================================"
	@echo "  Ejecutando PCA localmente..."
	@echo "======================================"
	./pca_program $(DATA_DIR)/input_data.csv $(DATA_DIR)/output_data.csv 2

# Validar resultados
validate:
	@echo "======================================"
	@echo "  Validando resultados..."
	@echo "======================================"
	@if not exist "$(REPORT_DIR)" mkdir "$(REPORT_DIR)"
	@if not exist "$(REPORT_DIR)/comparison_plots" mkdir "$(REPORT_DIR)/comparison_plots"
	cd $(PYTHON_DIR) && python validate_pca.py
	@echo ""
	@echo "Validacion completada. Ver resultados en $(REPORT_DIR)/"

# Limpiar archivos generados
clean:
	@echo "Limpiando archivos generados..."
	@if exist "$(DATA_DIR)\*.csv" del /Q "$(DATA_DIR)\*.csv"
	@if exist "$(DATA_DIR)\*.txt" del /Q "$(DATA_DIR)\*.txt"
	@if exist "$(REPORT_DIR)\*.png" del /Q "$(REPORT_DIR)\*.png"
	@if exist "$(REPORT_DIR)\*.txt" del /Q "$(REPORT_DIR)\*.txt"
	@if exist "$(SRC_DIR)\*.o" del /Q "$(SRC_DIR)\*.o"
	@if exist "$(SRC_DIR)\*.exe" del /Q "$(SRC_DIR)\*.exe"
	@if exist "$(SRC_DIR)\pca_program" del /Q "$(SRC_DIR)\pca_program"
	@echo "Archivos limpiados"

# Limpiar todo incluyendo Docker
clean-all: clean
	@echo "Eliminando contenedores e imagenes Docker..."
	-docker rm -f $(DOCKER_CONTAINER) 2>nul
	-docker rmi -f $(DOCKER_IMAGE) 2>nul
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

# Target para crear directorios necesarios
dirs:
	@if not exist "$(DATA_DIR)" mkdir "$(DATA_DIR)"
	@if not exist "$(REPORT_DIR)" mkdir "$(REPORT_DIR)"
	@if not exist "$(REPORT_DIR)\comparison_plots" mkdir "$(REPORT_DIR)\comparison_plots"
	@if not exist "$(SRC_DIR)" mkdir "$(SRC_DIR)"
	@echo "Directorios creados"

# Ayuda con ejemplos
examples:
	@echo "======================================"
	@echo "  Ejemplos de uso"
	@echo "======================================"
	@echo ""
	@echo "1. Flujo completo:"
	@echo "   make setup"
	@echo "   make generate-data"
	@echo "   make build"
	@echo "   make run"
	@echo "   make validate"
	@echo ""
	@echo "2. Generar datos personalizados:"
	@echo "   python python/generate_data.py --samples 1000 --features 20"
	@echo ""
	@echo "3. Solo validar (si ya tienes output_data.csv):"
	@echo "   make validate"
	@echo ""
