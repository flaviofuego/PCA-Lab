"""
Script para visualizar los datos sintéticos generados.
Crea gráficas exploratorias de los datos antes de aplicar PCA.

Autor: Lab PCA
Fecha: Octubre 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


def load_data(data_dir='../data'):
    """
    Carga los datos generados.
    
    Parámetros:
    -----------
    data_dir : str
        Directorio donde están los datos
        
    Retorna:
    --------
    X : numpy.ndarray
        Matriz de datos
    y : numpy.ndarray
        Etiquetas
    """
    data_path = Path(data_dir)
    
    X = np.loadtxt(data_path / 'input_data.csv', delimiter=',')
    y = np.loadtxt(data_path / 'labels.csv', delimiter=',')
    
    print(f"Datos cargados:")
    print(f"  - Shape: {X.shape}")
    print(f"  - Número de clases: {len(np.unique(y))}")
    
    return X, y


def plot_distributions(X, y, output_dir='../report/comparison_plots'):
    """
    Grafica las distribuciones de las primeras dimensiones.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Seleccionar primeras 4 dimensiones
    n_dims = min(4, X.shape[1])
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.ravel()
    
    for i in range(n_dims):
        ax = axes[i]
        
        # Histograma por clase
        for class_label in np.unique(y):
            mask = y == class_label
            ax.hist(X[mask, i], alpha=0.6, bins=30, 
                   label=f'Clase {int(class_label)}', density=True)
        
        ax.set_xlabel(f'Dimensión {i}')
        ax.set_ylabel('Densidad')
        ax.set_title(f'Distribución - Dimensión {i}')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path / 'data_distributions.png', dpi=300, bbox_inches='tight')
    print(f"✓ Gráfica guardada: {output_path / 'data_distributions.png'}")
    plt.close()


def plot_scatter_matrix(X, y, output_dir='../report/comparison_plots'):
    """
    Grafica matriz de dispersión de las primeras dimensiones.
    """
    output_path = Path(output_dir)
    
    # Seleccionar primeras 4 dimensiones
    n_dims = min(4, X.shape[1])
    df = pd.DataFrame(X[:, :n_dims], columns=[f'Dim_{i}' for i in range(n_dims)])
    df['Clase'] = y.astype(int)
    
    # Crear scatter plot matrix
    fig = plt.figure(figsize=(14, 12))
    
    # Usar pairplot de seaborn
    g = sns.pairplot(df, hue='Clase', diag_kind='hist', 
                     plot_kws={'alpha': 0.6, 's': 30},
                     diag_kws={'bins': 30, 'alpha': 0.7})
    
    g.fig.suptitle('Matriz de Dispersión - Datos Originales', y=1.01, fontsize=16)
    
    plt.savefig(output_path / 'scatter_matrix.png', dpi=300, bbox_inches='tight')
    print(f"✓ Gráfica guardada: {output_path / 'scatter_matrix.png'}")
    plt.close()


def plot_correlation_matrix(X, output_dir='../report/comparison_plots'):
    """
    Grafica la matriz de correlación de todas las dimensiones.
    """
    output_path = Path(output_dir)
    
    # Calcular matriz de correlación
    corr_matrix = np.corrcoef(X.T)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto', 
                   vmin=-1, vmax=1)
    
    # Configurar ticks
    n_dims = X.shape[1]
    ax.set_xticks(range(n_dims))
    ax.set_yticks(range(n_dims))
    ax.set_xticklabels([f'Dim {i}' for i in range(n_dims)], rotation=45)
    ax.set_yticklabels([f'Dim {i}' for i in range(n_dims)])
    
    # Añadir valores de correlación
    for i in range(n_dims):
        for j in range(n_dims):
            text = ax.text(j, i, f'{corr_matrix[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=8)
    
    ax.set_title('Matriz de Correlación entre Dimensiones', fontsize=14, pad=20)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Correlación', rotation=270, labelpad=20)
    
    plt.tight_layout()
    plt.savefig(output_path / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
    print(f"✓ Gráfica guardada: {output_path / 'correlation_matrix.png'}")
    plt.close()


def plot_3d_scatter(X, y, output_dir='../report/comparison_plots'):
    """
    Grafica dispersión 3D de las primeras 3 dimensiones.
    """
    output_path = Path(output_dir)
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot por clase
    for class_label in np.unique(y):
        mask = y == class_label
        ax.scatter(X[mask, 0], X[mask, 1], X[mask, 2], 
                  label=f'Clase {int(class_label)}',
                  alpha=0.6, s=30)
    
    ax.set_xlabel('Dimensión 0')
    ax.set_ylabel('Dimensión 1')
    ax.set_zlabel('Dimensión 2')
    ax.set_title('Visualización 3D - Primeras 3 Dimensiones', fontsize=14)
    ax.legend()
    
    plt.savefig(output_path / '3d_scatter.png', dpi=300, bbox_inches='tight')
    print(f"✓ Gráfica guardada: {output_path / '3d_scatter.png'}")
    plt.close()


def generate_summary_statistics(X, y, output_dir='../report'):
    """
    Genera estadísticas resumidas y las guarda en un archivo.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with open(output_path / 'data_summary.txt', 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("RESUMEN DE DATOS SINTÉTICOS GENERADOS\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Número de muestras: {X.shape[0]}\n")
        f.write(f"Número de dimensiones: {X.shape[1]}\n")
        f.write(f"Número de clases: {len(np.unique(y))}\n\n")
        
        f.write("Distribución de clases:\n")
        for class_label in np.unique(y):
            count = np.sum(y == class_label)
            percentage = (count / len(y)) * 100
            f.write(f"  Clase {int(class_label)}: {count} muestras ({percentage:.2f}%)\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("ESTADÍSTICAS POR DIMENSIÓN\n")
        f.write("=" * 70 + "\n\n")
        
        for i in range(X.shape[1]):
            f.write(f"Dimensión {i}:\n")
            f.write(f"  Media:              {X[:, i].mean():.6f}\n")
            f.write(f"  Desviación estándar: {X[:, i].std():.6f}\n")
            f.write(f"  Mínimo:             {X[:, i].min():.6f}\n")
            f.write(f"  Máximo:             {X[:, i].max():.6f}\n")
            f.write(f"  Mediana:            {np.median(X[:, i]):.6f}\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("MATRIZ DE COVARIANZA\n")
        f.write("=" * 70 + "\n\n")
        
        cov_matrix = np.cov(X.T)
        f.write("Valores en la diagonal (varianzas):\n")
        for i in range(X.shape[1]):
            f.write(f"  Dim {i}: {cov_matrix[i, i]:.6f}\n")
    
    print(f"✓ Resumen guardado: {output_path / 'data_summary.txt'}")


def main():
    """Función principal."""
    print("=" * 70)
    print("VISUALIZACIÓN DE DATOS SINTÉTICOS")
    print("=" * 70)
    print()
    
    # Cargar datos
    X, y = load_data()
    
    print("\nGenerando visualizaciones...")
    print()
    
    # Generar todas las gráficas
    plot_distributions(X, y)
    plot_correlation_matrix(X)
    plot_scatter_matrix(X, y)
    plot_3d_scatter(X, y)
    
    # Generar resumen estadístico
    generate_summary_statistics(X, y)
    
    print()
    print("=" * 70)
    print("✓ Visualización completada")
    print("=" * 70)
    print("\nGráficas guardadas en: report/comparison_plots/")
    print("Resumen guardado en: report/data_summary.txt")


if __name__ == '__main__':
    main()
