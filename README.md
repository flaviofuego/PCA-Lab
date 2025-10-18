# Laboratorio PCA - Implementación en C

Implementación del algoritmo **PCA (Principal Component Analysis)** en C desde cero, validada contra scikit-learn.

## 🚀 Uso Rápido

```bash
# Ejecutar todo el pipeline (generar datos + compilar + ejecutar + validar)
make all-steps

# Con parámetros personalizados
make all-steps SAMPLES=1000 FEATURES=10
```

Ver resultados en `report/validation_report.txt` y gráficas en `report/comparison_plots/`

---

## 📁 Estructura del Proyecto

```text
PCA-Lab/
├── data/                  # Datos de entrada/salida
├── python/                # Scripts Python (generar/validar)
├── src/                   # Código C (pca.c, pca.h, main.c)
├── report/                # Reportes y gráficas
├── Dockerfile             # Contenedor con GCC
└── Makefile               # Automatización
```

## 🔧 Comandos Disponibles

```bash
# Pipeline completo (con versionado automático)
make all-steps                           # Genera datos + compila + ejecuta + valida

# Con parámetros personalizados
make all-steps SAMPLES=1000 FEATURES=10  # 1000 muestras × 10 dimensiones
make all-steps SAMPLES=5000 FEATURES=25  # 5000 muestras × 25 dimensiones

# Elegir tipo de datos
make all-steps SAMPLES=1000 FEATURES=10 TYPE=classification  # Datos de clasificación (default)
make all-steps SAMPLES=1000 FEATURES=10 TYPE=blobs          # Datos con clusters

# Controlar componentes principales
make all-steps SAMPLES=1000 FEATURES=10 N_COMPONENTS=3      # Reducir a 3 componentes (default: 2)
make all-steps SAMPLES=1000 FEATURES=15 N_COMPONENTS=5      # Reducir a 5 componentes

# Control de versionado
make all-steps SAMPLES=1000 FEATURES=10 TIMESTAMP=true   # Con timestamp (default)
make all-steps SAMPLES=1000 FEATURES=10 TIMESTAMP=false  # Sin timestamp (sobrescribe)

# Pasos individuales
make generate-data                       # Solo generar datos
make build                               # Solo construir Docker
make run                                 # Solo ejecutar PCA
make validate                            # Solo validar resultados
make clean                               # Limpiar archivos generados
```

### 📊 Tipos de Datos

- **`TYPE=classification`** (default): Datos sintéticos de clasificación con características informativas y redundantes. Ideal para datasets realistas con múltiples dimensiones correlacionadas.

- **`TYPE=blobs`**: Datos agrupados en **clusters** bien definidos. Perfecto para:
  - Visualizar la separación de grupos después de PCA
  - Demostrar cómo PCA preserva la estructura de clusters
  - Validar que los componentes principales mantienen la agrupación natural
  
  Ejemplo de uso para datos con clusters:
  
  ```bash
  make all-steps SAMPLES=1000 FEATURES=10 TYPE=blobs
  ```
  
  Los clusters generados se distribuyen naturalmente en el espacio multidimensional, y PCA los proyecta preservando su separación en 2D.

### 🗂️ Versionado de Archivos

Por defecto (`TIMESTAMP=true`), **todo el pipeline** crea archivos versionados:

- **Entrada**: `input_data_20251016_143025.csv`, `labels_20251016_143025.csv`
- **Salida C**: `output_data_20251016_143025.csv`
- **Reportes**: `validation_report_20251016_143025.txt`, `numerical_comparison_20251016_143025.txt`
- **Gráficas**: `pca_comparison_scatter_20251016_143025.png`, etc.

Los archivos sin timestamp (`input_data.csv`, `output_data.csv`, etc.) siempre apuntan a la versión más reciente para uso del programa.

**Ventajas del versionado:**

- Preserva historial completo de experimentos
- Permite comparar resultados entre diferentes configuraciones
- No sobrescribe resultados anteriores accidentalmente

Para sobrescribir archivos sin versionado: `TIMESTAMP=false`

## 📊 ¿Qué hace el proyecto?

1. **Genera datos sintéticos** (Python): Crea dataset con N muestras y M dimensiones
2. **Reduce dimensionalidad** (C): Aplica PCA para reducir a 2 componentes principales
3. **Valida resultados** (Python): Compara con scikit-learn y genera gráficas

## 📈 Resultados

El proyecto genera:

- `data/input_data.csv` - Datos originales (N×M)
- `data/output_data.csv` - Datos reducidos (N×2)
- `report/validation_report.txt` - Reporte de validación
- `report/comparison_plots/*.png` - 8 gráficas comparativas

**Precisión:** Correlación perfecta (≈1.0) con scikit-learn

## 🐳 Tecnologías

- **Lenguaje**: C (implementación PCA)
- **Python**: Generación de datos y validación
- **Docker**: Entorno GCC reproducible
- **Make**: Automatización del pipeline
