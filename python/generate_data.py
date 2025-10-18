"""
Script para generar datos sintéticos para el laboratorio de PCA.
Genera un conjunto de datos con N muestras y M dimensiones, 
y los guarda en formato CSV para ser procesados por el algoritmo PCA en C.

Autor: Lab PCA
Fecha: Octubre 2025
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_blobs
from pathlib import Path
import argparse
from datetime import datetime

# Determinar rutas absolutas basadas en la ubicación del script
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / 'data'


def generate_synthetic_data(n_samples=500, n_features=10, n_informative=8, 
                           n_redundant=2, random_state=42):
    """
    Genera datos sintéticos usando sklearn.
    
    Parámetros:
    -----------
    n_samples : int
        Número de muestras a generar
    n_features : int
        Número de dimensiones (características) de los datos
    n_informative : int
        Número de características informativas
    n_redundant : int
        Número de características redundantes
    random_state : int
        Semilla para reproducibilidad
        
    Retorna:
    --------
    X : numpy.ndarray
        Matriz de datos de forma (n_samples, n_features)
    y : numpy.ndarray
        Etiquetas de clase (para referencia)
    """
    print(f"Generando datos sintéticos...")
    print(f"  - Muestras (N): {n_samples}")
    print(f"  - Dimensiones (M): {n_features}")
    print(f"  - Características informativas: {n_informative}")
    print(f"  - Características redundantes: {n_redundant}")
    
    # Generar datos de clasificación
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_redundant,
        n_clusters_per_class=2,
        random_state=random_state,
        shuffle=True
    )
    
    # Escalar los datos para hacerlos más realistas
    X = X * np.random.uniform(0.5, 2.0, size=n_features)
    X = X + np.random.uniform(-5, 5, size=n_features)
    
    print(f"  - Shape de los datos: {X.shape}")
    print(f"  - Media de cada dimensión: {X.mean(axis=0)[:3]}... (primeras 3)")
    print(f"  - Desviación estándar: {X.std(axis=0)[:3]}... (primeras 3)")
    
    return X, y


def generate_blobs_data(n_samples=500, n_features=10, centers=3, random_state=42):
    """
    Genera datos en forma de clusters usando make_blobs.
    Útil para visualizar la separación después de PCA.
    
    Parámetros:
    -----------
    n_samples : int
        Número de muestras
    n_features : int
        Número de dimensiones
    centers : int
        Número de clusters
    random_state : int
        Semilla para reproducibilidad
        
    Retorna:
    --------
    X : numpy.ndarray
        Matriz de datos
    y : numpy.ndarray
        Etiquetas de cluster
    """
    print(f"Generando datos de clusters...")
    print(f"  - Muestras (N): {n_samples}")
    print(f"  - Dimensiones (M): {n_features}")
    print(f"  - Número de clusters: {centers}")
    
    X, y = make_blobs(
        n_samples=n_samples,
        n_features=n_features,
        centers=centers,
        cluster_std=2.0,
        random_state=random_state
    )
    
    print(f"  - Shape de los datos: {X.shape}")
    
    return X, y


def save_to_csv(X, y, output_dir=None, filename='input_data.csv', 
                labels_filename='labels.csv', use_timestamp=False):
    """
    Guarda los datos en formato CSV.
    
    Parámetros:
    -----------
    X : numpy.ndarray
        Matriz de datos
    y : numpy.ndarray
        Etiquetas (se guardan por separado para referencia)
    output_dir : str or Path
        Directorio de salida (si es None, usa DATA_DIR por defecto)
    filename : str
        Nombre del archivo para los datos
    labels_filename : str
        Nombre del archivo para las etiquetas
    use_timestamp : bool
        Si es True, agrega timestamp a los nombres de archivo
    """
    # Usar DATA_DIR por defecto
    if output_dir is None:
        output_dir = DATA_DIR
    else:
        output_dir = Path(output_dir).resolve()
    
    # Crear directorio si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Agregar timestamp si es necesario
    if use_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = filename.replace('.csv', '')
        filename = f"{base_name}_{timestamp}.csv"
        
        base_labels = labels_filename.replace('.csv', '')
        labels_filename = f"{base_labels}_{timestamp}.csv"
    
    # Ruta completa del archivo
    filepath = output_dir / filename
    labels_filepath = output_dir / labels_filename
    
    # Guardar datos (sin encabezados, solo valores numéricos)
    # Formato: cada fila es una muestra, cada columna es una dimensión
    np.savetxt(filepath, X, delimiter=',', fmt='%.6f')
    print(f"\n✓ Datos guardados en: {filepath}")
    print(f"  - Formato: CSV sin encabezados")
    print(f"  - Dimensiones: {X.shape[0]} filas x {X.shape[1]} columnas")
    
    # Guardar etiquetas por separado (para validación)
    np.savetxt(labels_filepath, y, delimiter=',', fmt='%d')
    print(f"✓ Etiquetas guardadas en: {labels_filepath}")
    
    # También guardar una versión con pandas para inspección
    df = pd.DataFrame(X, columns=[f'dim_{i}' for i in range(X.shape[1])])
    df['label'] = y
    
    if use_timestamp:
        info_filename = f'input_data_with_labels_{timestamp}.csv'
    else:
        info_filename = 'input_data_with_labels.csv'
    
    info_filepath = output_dir / info_filename
    df.to_csv(info_filepath, index=False)
    print(f"✓ Datos con etiquetas (para inspección): {info_filepath}")
    
    # Solo crear enlaces si se usa timestamp (de lo contrario, los archivos ya son los "latest")
    if use_timestamp:
        # Siempre crear/actualizar enlaces simbólicos a los archivos más recientes
        # Esto permite que el programa en C siempre use los últimos datos
        latest_input = output_dir / 'input_data.csv'
        latest_labels = output_dir / 'labels.csv'
        latest_with_labels = output_dir / 'input_data_with_labels.csv'
        
        # En Windows, copiar en lugar de crear enlaces simbólicos
        import shutil
        shutil.copy2(filepath, latest_input)
        shutil.copy2(labels_filepath, latest_labels)
        shutil.copy2(info_filepath, latest_with_labels)
        
        print(f"\n✓ Enlaces a archivos actuales actualizados:")
        print(f"  - {latest_input}")
        print(f"  - {latest_labels}")
    
    return filepath, labels_filepath


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Genera datos sintéticos para el laboratorio de PCA'
    )
    parser.add_argument(
        '--samples', '-n', type=int, default=500,
        help='Número de muestras (default: 500)'
    )
    parser.add_argument(
        '--features', '-m', type=int, default=10,
        help='Número de dimensiones (default: 10)'
    )
    parser.add_argument(
        '--type', '-t', choices=['classification', 'blobs'], 
        default='classification',
        help='Tipo de datos a generar (default: classification)'
    )
    parser.add_argument(
        '--output', '-o', type=str, default=None,
        help=f'Directorio de salida (default: {DATA_DIR})'
    )
    parser.add_argument(
        '--timestamp', action='store_true',
        help='Agregar timestamp a los nombres de archivo para no sobrescribir'
    )
    
    args = parser.parse_args()
    
    # Si no se especifica output, usar DATA_DIR
    output_dir = Path(args.output).resolve() if args.output else DATA_DIR
    
    print("=" * 60)
    print("GENERACIÓN DE DATOS SINTÉTICOS PARA PCA")
    print("=" * 60)
    print(f"Directorio de salida: {output_dir}")
    print()
    
    # Generar datos según el tipo seleccionado
    if args.type == 'classification':
        X, y = generate_synthetic_data(
            n_samples=args.samples,
            n_features=args.features,
            n_informative=max(2, args.features - 2),
            n_redundant=min(2, args.features // 2)
        )
    else:  # blobs
        X, y = generate_blobs_data(
            n_samples=args.samples,
            n_features=args.features,
            centers=3
        )
    
    # Guardar datos con o sin timestamp
    save_to_csv(X, y, output_dir=output_dir, use_timestamp=args.timestamp)

    print("\n" + "✓ Generación completada exitosamente")
    print("=" * 60)
    
    if args.timestamp:
        print("\nModo: Archivos versionados con timestamp")
        print("  Los archivos input_data.csv y labels.csv apuntan a la versión más reciente")
    
    print("\nPróximos pasos:")
    print("  1. Revisar los datos en: data/input_data.csv")
    print("  2. Compilar y ejecutar el algoritmo PCA en C")
    print("  3. Validar los resultados con validate_pca.py")


if __name__ == '__main__':
    main()
