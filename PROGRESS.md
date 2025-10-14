# Resumen de la Generación de Datos Sintéticos

## ✅ Completado

Se ha implementado exitosamente la **Parte 1: Generación de Datos Sintéticos** del laboratorio de PCA.

## Archivos Creados

### 1. Scripts de Python
- **`python/generate_data.py`**: Script principal para generar datos sintéticos
  - Genera N muestras con M dimensiones
  - Configurable mediante argumentos de línea de comandos
  - Guarda datos en formato CSV sin encabezados (listo para C)
  - Genera estadísticas descriptivas

- **`python/visualize_data.py`**: Script para visualizar los datos generados
  - Genera 4 tipos de gráficas:
    - Distribuciones por dimensión
    - Matriz de correlación
    - Matriz de dispersión (scatter matrix)
    - Gráfica 3D de las primeras 3 dimensiones
  - Crea resumen estadístico detallado

- **`python/requirements.txt`**: Dependencias necesarias
  - numpy, scikit-learn, matplotlib, seaborn, pandas

### 2. Datos Generados
- **`data/input_data.csv`**: 500 muestras × 10 dimensiones
  - Formato: valores numéricos separados por comas
  - Sin encabezados (listo para lectura en C)
  
- **`data/labels.csv`**: Etiquetas de clase (para validación)
  - 2 clases balanceadas (250 muestras cada una)

- **`data/input_data_with_labels.csv`**: Datos con etiquetas para inspección

- **`data/data_statistics.txt`**: Estadísticas descriptivas

### 3. Visualizaciones
- **`report/comparison_plots/data_distributions.png`**: Histogramas de las primeras 4 dimensiones
- **`report/comparison_plots/correlation_matrix.png`**: Matriz de correlación completa
- **`report/comparison_plots/scatter_matrix.png`**: Matriz de dispersión pairplot
- **`report/comparison_plots/3d_scatter.png`**: Visualización 3D

- **`report/data_summary.txt`**: Resumen estadístico detallado

### 4. Infraestructura
- **`Dockerfile`**: Configuración para compilar C con GCC en Linux
- **`Makefile`**: Automatización de tareas (adaptado para Windows PowerShell)
- **`README.md`**: Documentación completa del proyecto
- **`.gitignore`**: Configuración de archivos a ignorar

## Características de los Datos Generados

### Configuración Actual
- **Número de muestras (N)**: 500
- **Número de dimensiones (M)**: 10
- **Tipo de datos**: Clasificación con 2 clases balanceadas
- **Características informativas**: 8
- **Características redundantes**: 2

### Estadísticas Clave
- Media por dimensión: varía entre -5.21 y 4.86
- Desviación estándar: varía entre 1.12 y 4.91
- Distribución balanceada: 50% clase 0, 50% clase 1
- Datos escalados y desplazados para mayor realismo

## Cómo Usar

### Generar Nuevos Datos
```powershell
# Configuración por defecto (500 muestras, 10 dimensiones)
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/generate_data.py

# Configuración personalizada
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/generate_data.py --samples 1000 --features 20

# Generar datos tipo clusters
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/generate_data.py --type blobs --samples 500
```

### Visualizar Datos
```powershell
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/visualize_data.py
```

### Usando Make (simplificado)
```powershell
# Instalar dependencias
make setup

# Generar datos
make generate-data
```

## Formato de los Datos para C

Los datos en `input_data.csv` tienen el siguiente formato:

```
5.694423,3.104160,-5.078643,5.802416,...
6.025506,0.473017,0.812817,4.569351,...
...
```

- **Sin encabezados**: Solo valores numéricos
- **Separador**: Coma (`,`)
- **Formato numérico**: Punto decimal (`.`)
- **Precisión**: 6 decimales
- **Estructura**: Cada fila es una muestra, cada columna es una dimensión

Este formato es ideal para leer en C usando funciones como `fscanf()` o `fgets()` con `strtok()`.

## Próximos Pasos

1. **Implementar PCA en C** (Siguiente fase)
   - Leer datos desde `data/input_data.csv`
   - Implementar algoritmo PCA:
     - Centrar datos (restar media)
     - Calcular matriz de covarianza
     - Calcular eigenvectores y eigenvalores
     - Proyectar datos a K dimensiones
   - Guardar resultados en `data/output_data.csv`

2. **Validar con sklearn** (Fase final)
   - Comparar resultados numéricos
   - Generar gráficas de comparación
   - Elaborar reporte final

## Notas Técnicas

### Entorno de Desarrollo
- **Sistema Operativo**: Windows
- **Shell**: PowerShell v5.1
- **Python**: 3.10.6 (entorno virtual)
- **Compilador C** (próximo): GCC via Docker

### Reproducibilidad
- Se usa `random_state=42` para resultados reproducibles
- Los mismos parámetros generarán siempre los mismos datos
- Útil para debugging y validación

### Extensibilidad
El código está diseñado para ser fácilmente modificable:
- Cambiar número de muestras y dimensiones
- Agregar nuevos tipos de datos sintéticos
- Modificar estadísticas de generación
- Añadir más visualizaciones

---

**Estado**: ✅ Fase 1 Completada
**Fecha**: 14 de octubre de 2025
**Siguiente**: Implementación de PCA en C
