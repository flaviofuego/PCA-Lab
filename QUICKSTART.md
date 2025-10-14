# Guía Rápida - Laboratorio PCA

## 🎯 Resumen Ejecutivo

Se ha completado exitosamente la **Fase 1: Generación de Datos Sintéticos** del laboratorio de PCA.

### ✅ Lo que se ha logrado:
1. ✓ Scripts Python para generar datos sintéticos
2. ✓ 500 muestras con 10 dimensiones generadas
3. ✓ Datos guardados en formato CSV (listo para C)
4. ✓ Visualizaciones completas de los datos
5. ✓ Infraestructura Docker y Makefile preparada
6. ✓ Documentación completa

---

## 📁 Estructura del Proyecto

```
PCA-Lab/
├── data/                           # Datos generados ✓
│   ├── input_data.csv             # 500×10 datos para PCA
│   ├── labels.csv                 # Etiquetas de clase
│   ├── input_data_with_labels.csv # Datos + etiquetas
│   └── data_statistics.txt        # Estadísticas descriptivas
│
├── python/                         # Scripts Python ✓
│   ├── generate_data.py           # Generador de datos sintéticos
│   ├── visualize_data.py          # Visualizaciones
│   ├── examples.py                # Ejemplos de uso
│   ├── validate_pca.py            # (Pendiente - Fase 3)
│   └── requirements.txt           # Dependencias
│
├── src/                            # Código C (Pendiente - Fase 2)
│   ├── pca.h                      # (Por implementar)
│   ├── pca.c                      # (Por implementar)
│   └── main.c                     # (Por implementar)
│
├── report/                         # Reportes y visualizaciones ✓
│   ├── data_summary.txt           # Resumen estadístico
│   └── comparison_plots/          # Gráficas
│       ├── data_distributions.png
│       ├── correlation_matrix.png
│       ├── scatter_matrix.png
│       └── 3d_scatter.png
│
├── Dockerfile                      # Configuración Docker ✓
├── Makefile                        # Automatización ✓
├── README.md                       # Documentación principal ✓
├── PROGRESS.md                     # Progreso detallado ✓
└── QUICKSTART.md                   # Esta guía ✓
```

---

## 🚀 Comandos Rápidos

### Instalación Inicial
```powershell
# Instalar dependencias Python
make setup
```

### Generar Datos
```powershell
# Opción 1: Usando Make
make generate-data

# Opción 2: Comando directo (configuración default)
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/generate_data.py

# Opción 3: Configuración personalizada
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/generate_data.py --samples 1000 --features 20
```

### Visualizar Datos
```powershell
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/visualize_data.py
```

### Ver Ejemplos
```powershell
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/examples.py
```

---

## 📊 Datos Generados

### Características
- **Tamaño**: 500 muestras × 10 dimensiones
- **Formato**: CSV sin encabezados
- **Tipo**: Datos de clasificación con 2 clases balanceadas
- **Ubicación**: `data/input_data.csv`

### Estadísticas Clave
```
Número de muestras (N): 500
Número de dimensiones (M): 10
Clases: 2 (250 muestras cada una, 50% balance)

Media por dimensión: [-0.08, -5.32, -2.10, 3.09, -3.10, 1.56, 1.13, -3.89, -2.17, -0.59]
Desviación estándar:  [3.55, 3.11, 3.01, 4.50, 2.15, 3.60, 1.30, 1.13, 2.12, 3.28]
```

### Formato del CSV
```csv
2.547295,-4.253115,-4.415565,5.316004,-2.227387,4.306645,-0.037720,-3.604710,-2.198711,-2.401035
3.594536,-8.850169,0.376699,4.186284,-1.123087,0.512897,0.377669,-4.544322,-2.399228,-3.510747
...
```

---

## 📈 Visualizaciones Generadas

1. **Distribuciones** (`data_distributions.png`)
   - Histogramas de las primeras 4 dimensiones
   - Separación por clases

2. **Matriz de Correlación** (`correlation_matrix.png`)
   - Correlaciones entre todas las dimensiones
   - Útil para entender dependencias

3. **Scatter Matrix** (`scatter_matrix.png`)
   - Dispersión 2D entre pares de dimensiones
   - Vista completa de relaciones

4. **Gráfica 3D** (`3d_scatter.png`)
   - Visualización 3D de primeras 3 dimensiones
   - Separación de clases en 3D

---

## 🔧 Próximos Pasos

### Fase 2: Implementar PCA en C (Pendiente)

El algoritmo debe:
1. Leer datos de `data/input_data.csv`
2. Implementar PCA:
   ```
   a. Centrar datos (restar media)
   b. Calcular matriz de covarianza
   c. Calcular eigenvectores y eigenvalores
   d. Ordenar por eigenvalores (descendente)
   e. Seleccionar K componentes principales
   f. Proyectar datos al nuevo espacio
   ```
3. Guardar resultados en `data/output_data.csv`

### Estructura Sugerida en C:
```c
// pca.h
typedef struct {
    double **data;
    int n_samples;
    int n_features;
} Matrix;

void center_data(Matrix *data);
void compute_covariance(Matrix *data, Matrix *cov);
void compute_eigen(Matrix *cov, double *eigenvalues, Matrix *eigenvectors);
void project_data(Matrix *data, Matrix *eigenvectors, int k, Matrix *output);
```

### Compilación con Docker:
```powershell
# Construir imagen
make build

# Ejecutar PCA
make run
```

### Fase 3: Validar con sklearn (Pendiente)

Crear `python/validate_pca.py` que:
1. Lea `data/output_data.csv` (resultado de C)
2. Ejecute PCA con sklearn
3. Compare resultados numéricos
4. Genere gráficas de comparación
5. Cree reporte final

---

## 📝 Información del Entorno

### Sistema
- **OS**: Windows
- **Shell**: PowerShell v5.1
- **Python**: 3.10.6 (entorno virtual)

### Dependencias Instaladas
- numpy >= 1.21.0
- scikit-learn >= 1.0.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0
- pandas >= 1.3.0

### Docker (para Fase 2)
- **Imagen base**: gcc:latest
- **Compilador**: GCC
- **Sistema**: Linux (dentro del contenedor)

---

## 💡 Ejemplos de Uso

### Generar diferentes tipos de datos:
```powershell
# Datos de clasificación (default)
python python/generate_data.py --type classification --samples 500 --features 10

# Datos de clusters
python python/generate_data.py --type blobs --samples 1000 --features 5

# Muchas dimensiones para PCA más interesante
python python/generate_data.py --samples 800 --features 50
```

### Personalizar K (dimensiones de salida):
En la implementación de C, K será un parámetro. Por ahora, en el ejemplo de sklearn:
- K=2: Visualización 2D fácil
- K=3: Visualización 3D
- K depende de la varianza acumulada deseada (típicamente 90-95%)

---

## 🐛 Solución de Problemas

### Error: "Module not found"
```powershell
# Reinstalar dependencias
pip install -r python/requirements.txt
```

### Error: "File not found"
```powershell
# Verificar que estás en el directorio raíz
cd "E:\Repos Git\PCA-Lab"

# Verificar archivos
ls data/
```

### Error: Docker no responde
```powershell
# Verificar que Docker Desktop está corriendo
docker --version
docker ps
```

---

## 📚 Referencias

### Algoritmo PCA
1. Centrar datos: `X_centered = X - mean(X)`
2. Covarianza: `Cov = (X_centered^T × X_centered) / (n-1)`
3. Eigen-descomposición: `Cov = V × Λ × V^T`
4. Proyección: `X_pca = X_centered × V[:, :k]`

### Archivos Clave
- `python/examples.py`: Muestra todos los pasos del algoritmo
- `data/data_statistics.txt`: Estadísticas de entrada
- `report/data_summary.txt`: Resumen completo

---

## ✅ Checklist de Progreso

### Fase 1: Generación de Datos ✓
- [x] Scripts de generación
- [x] Datos sintéticos (500×10)
- [x] Visualizaciones
- [x] Estadísticas descriptivas
- [x] Documentación

### Fase 2: Implementación en C (Siguiente)
- [ ] Estructura de datos en C
- [ ] Lectura de CSV
- [ ] Centrado de datos
- [ ] Matriz de covarianza
- [ ] Eigen-descomposición
- [ ] Proyección
- [ ] Escritura de resultados
- [ ] Dockerfile funcional
- [ ] Makefile con comandos

### Fase 3: Validación (Final)
- [ ] Script de validación
- [ ] Comparación numérica
- [ ] Gráficas comparativas
- [ ] Reporte final
- [ ] Documentación completa

---

**Estado Actual**: ✅ Fase 1 Completada (Generación de Datos)  
**Siguiente**: 🔨 Fase 2 (Implementación PCA en C)  
**Fecha**: 14 de octubre de 2025
