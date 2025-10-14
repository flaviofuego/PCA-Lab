# Laboratorio PCA - Implementación en C

## Descripción
Implementación de un algoritmo de Análisis de Componentes Principales (PCA) en lenguaje C que proyecta datos de M dimensiones a K dimensiones.

## Estructura del Proyecto
```
.
├── data/                  # Datos de entrada y salida
│   ├── input_data.csv    # Datos sintéticos generados
│   └── output_data.csv   # Datos proyectados por PCA en C
├── python/               # Scripts de Python
│   ├── generate_data.py  # Generación de datos sintéticos
│   ├── validate_pca.py   # Validación y comparación
│   └── requirements.txt  # Dependencias de Python
├── src/                  # Código fuente en C
│   ├── pca.c            # Implementación del algoritmo PCA
│   ├── pca.h            # Archivo de cabecera
│   └── main.c           # Programa principal
├── Dockerfile           # Configuración de Docker para compilación
├── Makefile            # Automatización de tareas
└── report/             # Documentación y resultados
    └── comparison_plots/ # Gráficas de comparación
```

## Requisitos
- Docker
- Python 3.8+
- Make (opcional, pero recomendado)

## Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd PCA-Lab
```

### 2. Instalar dependencias de Python
```bash
pip install -r python/requirements.txt
```

## Uso

### Generar datos sintéticos
```bash
python python/generate_data.py
```

### Compilar y ejecutar PCA en C (usando Docker)
```bash
make build    # Construir la imagen Docker
make run      # Ejecutar el algoritmo PCA
```

### Validar resultados
```bash
python python/validate_pca.py
```

### Limpiar archivos generados
```bash
make clean
```

## Entorno de Desarrollo
- **Sistema Operativo**: Windows
- **Compilador**: GCC (via Docker)
- **Shell**: PowerShell v5.1
- **Python**: 3.8+

## Metodología PCA
1. Centrar los datos (restar la media)
2. Calcular la matriz de covarianza
3. Calcular eigenvectores y eigenvalores
4. Ordenar eigenvectores por eigenvalores descendentes
5. Seleccionar K componentes principales
6. Proyectar los datos en el nuevo espacio

## Resultados
Los resultados de la comparación entre la implementación en C y sklearn se encuentran en la carpeta `report/`.
