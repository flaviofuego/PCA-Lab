# GUÍA DE EJECUCIÓN - PCA LAB

## 🚀 Método 1: Pipeline Completo (Recomendado)

```bash
# Setup inicial (solo primera vez)
make setup

# Ejecutar todo
make all-steps
```

**Resultado:** Genera datos → Compila → Ejecuta → Valida  
**Tiempo:** ~2-3 minutos  
**Ver resultados:** `report/validation_report.txt`

---

## 📝 Método 2: Paso a Paso

### 1. Instalar dependencias Python
```bash
make setup
```

### 2. Generar datos sintéticos
```bash
make generate-data
```
**Salida:** `data/input_data.csv` (500×10)

### 3. Compilar y ejecutar PCA en C
```bash
make build    # Construir imagen Docker
make run      # Ejecutar PCA
```
**Salida:** `data/output_data.csv` (500×2)

### 4. Validar resultados
```bash
make validate
```
**Salida:** `report/validation_report.txt` + 5 gráficas

---

## 💻 Método 3: Sin Make

### Windows PowerShell:
```powershell
# 1. Setup
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r python/requirements.txt

# 2. Generar datos
& .venv\Scripts\python.exe python/generate_data.py

# 3. Compilar y ejecutar
docker build -t pca-lab-gcc .
docker run --rm -v "${PWD}/data:/app/data" -v "${PWD}/src:/app/src" pca-lab-gcc

# 4. Validar
& .venv\Scripts\python.exe python/validate_pca.py
```

### Linux/Mac:
```bash
# 1. Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r python/requirements.txt

# 2. Generar datos
python3 python/generate_data.py

# 3. Compilar y ejecutar
docker build -t pca-lab-gcc .
docker run --rm -v "$(pwd)/data:/app/data" -v "$(pwd)/src:/app/src" pca-lab-gcc

# 4. Validar
python3 python/validate_pca.py
```

---

## 🔍 Ver Resultados

```bash
# Reporte ejecutivo
cat report/validation_report.txt

# Métricas numéricas
cat report/numerical_comparison.txt

# Listar gráficas
ls report/comparison_plots/
```

---

## ⚡ Compilación Local (Alternativa sin Docker)

**Requiere:** GCC instalado (MinGW en Windows)

```bash
# Windows
.\compile.ps1
.\pca_program.exe data\input_data.csv data\output_data.csv 2

# Linux/Mac
gcc -o pca_program src/main.c src/pca.c -lm -O2 -Wall
./pca_program data/input_data.csv data/output_data.csv 2
```

---

## 🎯 Comandos Útiles

```bash
make help        # Mostrar ayuda
make clean       # Limpiar archivos generados
make clean-all   # Limpiar todo + Docker
```
