"""
Script de ejemplo que muestra cómo leer los datos generados.
Útil como referencia para la implementación en C.

Autor: Lab PCA
Fecha: Octubre 2025
"""

import numpy as np
import pandas as pd


def example_read_csv():
    """
    Ejemplo de cómo leer el archivo CSV generado.
    Simula lo que se hará en C.
    """
    print("=" * 70)
    print("EJEMPLO: Lectura de Datos CSV")
    print("=" * 70)
    print()
    
    # Método 1: Usando numpy (más eficiente)
    print("Método 1: Usando numpy.loadtxt()")
    print("-" * 70)
    
    data = np.loadtxt('../data/input_data.csv', delimiter=',')
    
    print(f"Shape de los datos: {data.shape}")
    print(f"Tipo de datos: {data.dtype}")
    print()
    print("Primeras 5 filas:")
    print(data[:5])
    print()
    
    # Método 2: Usando pandas (más conveniente para análisis)
    print("\nMétodo 2: Usando pandas.read_csv()")
    print("-" * 70)
    
    df = pd.read_csv('../data/input_data.csv', header=None)
    print(f"Shape: {df.shape}")
    print()
    print("Primeras 5 filas:")
    print(df.head())
    print()
    
    # Método 3: Lectura manual (similar a C)
    print("\nMétodo 3: Lectura línea por línea (similar a C)")
    print("-" * 70)
    
    with open('../data/input_data.csv', 'r') as f:
        lines = f.readlines()[:5]  # Solo primeras 5 líneas
        
        print(f"Número total de líneas: {len(lines)}")
        print()
        
        for i, line in enumerate(lines):
            values = line.strip().split(',')
            values_float = [float(v) for v in values]
            print(f"Línea {i}: {len(values_float)} valores")
            print(f"  Primeros 5 valores: {values_float[:5]}")


def example_statistics():
    """
    Calcula estadísticas básicas de los datos.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO: Estadísticas Básicas")
    print("=" * 70)
    print()
    
    data = np.loadtxt('../data/input_data.csv', delimiter=',')
    
    print(f"Número de muestras (filas): {data.shape[0]}")
    print(f"Número de dimensiones (columnas): {data.shape[1]}")
    print()
    
    print("Media por dimensión:")
    print(data.mean(axis=0))
    print()
    
    print("Desviación estándar por dimensión:")
    print(data.std(axis=0))
    print()
    
    print("Rango por dimensión (min, max):")
    for i in range(data.shape[1]):
        print(f"  Dim {i}: [{data[:, i].min():.4f}, {data[:, i].max():.4f}]")


def example_data_centering():
    """
    Ejemplo de cómo centrar los datos (primer paso de PCA).
    """
    print("\n" + "=" * 70)
    print("EJEMPLO: Centrado de Datos (Primer paso de PCA)")
    print("=" * 70)
    print()
    
    data = np.loadtxt('../data/input_data.csv', delimiter=',')
    
    print("Datos originales:")
    print(f"  Media de la primera dimensión: {data[:, 0].mean():.6f}")
    print(f"  Primeros 5 valores: {data[:5, 0]}")
    print()
    
    # Centrar los datos
    mean = data.mean(axis=0)
    data_centered = data - mean
    
    print("Datos centrados (restando la media):")
    print(f"  Nueva media de la primera dimensión: {data_centered[:, 0].mean():.10f}")
    print(f"  Primeros 5 valores: {data_centered[:5, 0]}")
    print()
    
    print("Nota: La media debe ser muy cercana a 0 (puede tener pequeños errores de redondeo)")


def example_covariance_matrix():
    """
    Ejemplo de cómo calcular la matriz de covarianza.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO: Matriz de Covarianza (Segundo paso de PCA)")
    print("=" * 70)
    print()
    
    data = np.loadtxt('../data/input_data.csv', delimiter=',')
    
    # Centrar los datos
    mean = data.mean(axis=0)
    data_centered = data - mean
    
    # Calcular matriz de covarianza
    # Método 1: Usando numpy
    cov_matrix = np.cov(data_centered.T)
    
    print(f"Shape de la matriz de covarianza: {cov_matrix.shape}")
    print("(Debe ser M×M, donde M es el número de dimensiones)")
    print()
    
    print("Matriz de covarianza (primeras 3×3 elementos):")
    print(cov_matrix[:3, :3])
    print()
    
    # Método 2: Cálculo manual (como se haría en C)
    n = data_centered.shape[0]
    m = data_centered.shape[1]
    
    cov_manual = np.dot(data_centered.T, data_centered) / (n - 1)
    
    print("Verificación (cálculo manual):")
    print("Las dos matrices deben ser iguales:")
    print(f"  Diferencia máxima: {np.max(np.abs(cov_matrix - cov_manual)):.10f}")
    print()
    
    print("Valores en la diagonal (varianzas):")
    for i in range(min(5, m)):
        print(f"  Dim {i}: {cov_matrix[i, i]:.6f}")


def example_pca_preview():
    """
    Vista previa de lo que hará PCA usando sklearn.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO: Vista Previa de PCA con sklearn")
    print("=" * 70)
    print()
    
    from sklearn.decomposition import PCA
    
    data = np.loadtxt('../data/input_data.csv', delimiter=',')
    
    # Aplicar PCA reduciendo a 2 dimensiones
    k = 2
    pca = PCA(n_components=k)
    data_pca = pca.fit_transform(data)
    
    print(f"Datos originales: {data.shape}")
    print(f"Datos después de PCA: {data_pca.shape}")
    print()
    
    print(f"Varianza explicada por cada componente:")
    for i, var in enumerate(pca.explained_variance_ratio_):
        print(f"  PC{i+1}: {var*100:.2f}%")
    print(f"  Total: {sum(pca.explained_variance_ratio_)*100:.2f}%")
    print()
    
    print("Primeras 5 muestras proyectadas:")
    print(data_pca[:5])
    print()
    
    print("Componentes principales (eigenvectores):")
    print("Shape:", pca.components_.shape)
    print("(K × M, donde K=componentes principales, M=dimensiones originales)")


def main():
    """Función principal."""
    example_read_csv()
    example_statistics()
    example_data_centering()
    example_covariance_matrix()
    example_pca_preview()
    
    print("\n" + "=" * 70)
    print("✓ Ejemplos completados")
    print("=" * 70)
    print("\nEstos ejemplos muestran:")
    print("  1. Cómo leer datos CSV (útil para C)")
    print("  2. Cómo calcular estadísticas básicas")
    print("  3. Cómo centrar los datos (restar media)")
    print("  4. Cómo calcular matriz de covarianza")
    print("  5. Vista previa del resultado esperado de PCA")


if __name__ == '__main__':
    main()
