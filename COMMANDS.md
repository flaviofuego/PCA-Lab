# Comandos Rápidos para Windows PowerShell

## 🚀 Inicio Rápido

### 1. Navegar al proyecto
```powershell
cd "E:\Repos Git\PCA-Lab"
```

### 2. Instalar dependencias Python
```powershell
# Activar entorno virtual (ya creado)
.\.venv\Scripts\Activate.ps1

# O usar directamente el intérprete
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" -m pip install -r python/requirements.txt
```

### 3. Generar datos sintéticos
```powershell
# Usando el comando directo
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/generate_data.py

# Con parámetros personalizados
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/generate_data.py --samples 1000 --features 20

# Generar clusters
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/generate_data.py --type blobs
```

### 4. Visualizar datos
```powershell
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/visualize_data.py
```

### 5. Ver ejemplos de procesamiento
```powershell
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/examples.py
```

---

## 📁 Explorar Archivos

### Ver estructura del proyecto
```powershell
tree /F
```

### Listar solo archivos principales
```powershell
Get-ChildItem -Path data,python,report -Recurse -File | Select-Object Directory, Name, Length
```

### Ver primeras líneas de datos
```powershell
Get-Content data/input_data.csv -TotalCount 10
```

### Ver estadísticas
```powershell
Get-Content data/data_statistics.txt
```

### Ver resumen
```powershell
Get-Content report/data_summary.txt
```

---

## 🐳 Docker (para Fase 2)

### Construir imagen
```powershell
docker build -t pca-lab-gcc .
```

### Ejecutar contenedor
```powershell
docker run --rm -v "${PWD}/data:/app/data" -v "${PWD}/src:/app/src" pca-lab-gcc
```

### Ver imágenes Docker
```powershell
docker images | Select-String "pca-lab"
```

### Limpiar contenedores e imágenes
```powershell
docker rm -f pca-lab-container
docker rmi -f pca-lab-gcc
```

---

## 🔍 Inspección de Datos

### Contar filas en CSV
```powershell
(Get-Content data/input_data.csv).Length
```

### Ver dimensiones de los datos
```powershell
$firstLine = Get-Content data/input_data.csv -TotalCount 1
$dimensions = ($firstLine -split ',').Length
$rows = (Get-Content data/input_data.csv).Length
Write-Host "Dimensiones: $rows x $dimensions"
```

### Ver distribución de clases
```powershell
$labels = Get-Content data/labels.csv
$class0 = ($labels | Where-Object {$_ -eq '0'}).Count
$class1 = ($labels | Where-Object {$_ -eq '1'}).Count
Write-Host "Clase 0: $class0 muestras"
Write-Host "Clase 1: $class1 muestras"
```

---

## 📊 Abrir Visualizaciones

### Con visualizador de imágenes por defecto
```powershell
Start-Process "report/comparison_plots/scatter_matrix.png"
Start-Process "report/comparison_plots/correlation_matrix.png"
Start-Process "report/comparison_plots/data_distributions.png"
Start-Process "report/comparison_plots/3d_scatter.png"
```

### Abrir todas las gráficas
```powershell
Get-ChildItem "report/comparison_plots/*.png" | ForEach-Object { Start-Process $_.FullName }
```

---

## 🧹 Limpieza

### Limpiar solo datos generados
```powershell
Remove-Item data/*.csv
Remove-Item data/*.txt -Exclude .gitkeep
Remove-Item report/*.txt
Remove-Item report/comparison_plots/*.png
```

### Limpiar todo (incluyendo venv)
```powershell
Remove-Item -Recurse -Force .venv
Remove-Item -Recurse -Force data/*
Remove-Item -Recurse -Force report/comparison_plots/*
```

---

## 📝 Git (Control de Versiones)

### Ver estado
```powershell
git status
```

### Agregar archivos
```powershell
git add python/*.py
git add README.md PROGRESS.md QUICKSTART.md
git add Makefile Dockerfile .gitignore
```

### Commit
```powershell
git commit -m "Fase 1: Generación de datos sintéticos completada"
```

### Push
```powershell
git push origin main
```

---

## 🔧 Troubleshooting

### Si hay problemas con el entorno virtual
```powershell
# Crear nuevo entorno
python -m venv .venv

# Activar
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r python/requirements.txt
```

### Si hay problemas con Docker
```powershell
# Verificar que Docker está corriendo
docker --version
docker ps

# Reiniciar Docker Desktop si es necesario
```

### Si hay errores de codificación en archivos
```powershell
# Leer archivo con codificación UTF-8
Get-Content -Path data/data_statistics.txt -Encoding UTF8
```

---

## 💡 Atajos Útiles

### Alias para comandos frecuentes
```powershell
# Agregar a tu perfil de PowerShell
New-Alias -Name pca-python -Value "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe"

# Uso
pca-python python/generate_data.py
```

### Función para generar datos rápido
```powershell
function Generate-PCAData {
    param(
        [int]$samples = 500,
        [int]$features = 10,
        [string]$type = "classification"
    )
    & "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/generate_data.py --samples $samples --features $features --type $type
}

# Uso
Generate-PCAData -samples 1000 -features 20
```

---

## 📚 Recursos Adicionales

### Documentación
- `README.md` - Documentación completa del proyecto
- `QUICKSTART.md` - Guía rápida
- `PROGRESS.md` - Progreso detallado del proyecto

### Ejemplos de Código
- `python/examples.py` - Ejemplos de lectura y procesamiento
- `python/generate_data.py` - Generación de datos con comentarios

### Ver ayuda de scripts
```powershell
& "E:/Repos Git/PCA-Lab/.venv/Scripts/python.exe" python/generate_data.py --help
```

---

## 🎯 Siguiente Fase: Implementación en C

### Archivos a crear:
1. `src/pca.h` - Declaraciones
2. `src/pca.c` - Implementación del algoritmo
3. `src/main.c` - Programa principal
4. `python/validate_pca.py` - Validación con sklearn

### Comando de compilación (manual):
```powershell
gcc -o pca_program src/*.c -lm -O2
```

### Ejecutar:
```powershell
./pca_program
```

---

**Nota**: Todos estos comandos asumen que estás en el directorio raíz del proyecto.
