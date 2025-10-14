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
import os
from pathlib import Path
import argparse

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
                labels_filename='labels.csv'):
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
    """
    # Usar DATA_DIR por defecto
    if output_dir is None:
        output_dir = DATA_DIR
    else:
        output_dir = Path(output_dir).resolve()
    
    # Crear directorio si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
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
    info_filepath = output_dir / 'input_data_with_labels.csv'
    df.to_csv(info_filepath, index=False)
    print(f"✓ Datos con etiquetas (para inspección): {info_filepath}")


def generate_statistics(X, output_dir=None):
    """
    Genera estadísticas descriptivas de los datos.
    
    Parámetros:
    -----------
    X : numpy.ndarray
        Matriz de datos
    output_dir : str or Path
        Directorio de salida (si es None, usa DATA_DIR por defecto)
    """
    # Usar DATA_DIR por defecto
    if output_dir is None:
        output_dir = DATA_DIR
    else:
        output_dir = Path(output_dir).resolve()
    
    stats_filepath = output_dir / 'data_statistics.txt'
    
    with open(stats_filepath, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("ESTADÍSTICAS DE LOS DATOS GENERADOS\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Número de muestras (N): {X.shape[0]}\n")
        f.write(f"Número de dimensiones (M): {X.shape[1]}\n\n")
        
        f.write("Media por dimensión:\n")
        for i, mean_val in enumerate(X.mean(axis=0)):
            f.write(f"  Dim {i}: {mean_val:.6f}\n")
        
        f.write("\nDesviación estándar por dimensión:\n")
        for i, std_val in enumerate(X.std(axis=0)):
            f.write(f"  Dim {i}: {std_val:.6f}\n")
        
        f.write("\nValor mínimo por dimensión:\n")
        for i, min_val in enumerate(X.min(axis=0)):
            f.write(f"  Dim {i}: {min_val:.6f}\n")
        
        f.write("\nValor máximo por dimensión:\n")
        for i, max_val in enumerate(X.max(axis=0)):
            f.write(f"  Dim {i}: {max_val:.6f}\n")
    
    print(f"✓ Estadísticas guardadas en: {stats_filepath}")


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
    
    # Guardar datos
    save_to_csv(X, y, output_dir=output_dir)
    
    # Generar estadísticas
    generate_statistics(X, output_dir=output_dir)
    
    print("\n" + "=" * 60)
    print("✓ Generación completada exitosamente")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("  1. Revisar los datos en: data/input_data.csv")
    print("  2. Compilar y ejecutar el algoritmo PCA en C")
    print("  3. Validar los resultados con validate_pca.py")


if __name__ == '__main__':
    main()
