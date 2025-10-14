"""
Script de validación para comparar la implementación de PCA en C con sklearn.
Realiza comparaciones numéricas y gráficas de los resultados.

Autor: Lab PCA
Fecha: Octubre 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, mean_absolute_error
from pathlib import Path
import sys

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10


def load_data(data_dir='../data'):
    """
    Carga los datos de entrada y salida.
    
    Returns:
    --------
    X_input : numpy.ndarray
        Datos de entrada originales
    X_c : numpy.ndarray
        Datos proyectados por PCA en C
    y : numpy.ndarray
        Etiquetas (para visualización)
    """
    data_path = Path(data_dir)
    
    print("=" * 70)
    print("CARGANDO DATOS")
    print("=" * 70)
    
    # Cargar datos de entrada
    X_input = np.loadtxt(data_path / 'input_data.csv', delimiter=',')
    print(f"✓ Datos de entrada cargados: {X_input.shape}")
    
    # Cargar datos proyectados por C
    X_c = np.loadtxt(data_path / 'output_data.csv', delimiter=',')
    print(f"✓ Datos de salida (C) cargados: {X_c.shape}")
    
    # Cargar etiquetas
    y = np.loadtxt(data_path / 'labels.csv', delimiter=',')
    print(f"✓ Etiquetas cargadas: {y.shape}")
    
    return X_input, X_c, y


def apply_sklearn_pca(X, n_components=2):
    """
    Aplica PCA usando sklearn.
    
    Parameters:
    -----------
    X : numpy.ndarray
        Datos de entrada
    n_components : int
        Número de componentes principales
        
    Returns:
    --------
    X_sklearn : numpy.ndarray
        Datos proyectados por sklearn
    pca : PCA
        Modelo PCA entrenado
    """
    print("\n" + "=" * 70)
    print("APLICANDO PCA CON SKLEARN")
    print("=" * 70)
    
    pca = PCA(n_components=n_components)
    X_sklearn = pca.fit_transform(X)
    
    print(f"✓ PCA sklearn aplicado")
    print(f"  - Shape: {X_sklearn.shape}")
    print(f"  - Varianza explicada: {pca.explained_variance_ratio_.sum():.4f} ({pca.explained_variance_ratio_.sum()*100:.2f}%)")
    print(f"  - Componentes principales:")
    for i, var in enumerate(pca.explained_variance_ratio_):
        print(f"    PC{i+1}: {var*100:.2f}%")
    
    return X_sklearn, pca


def compare_numerical(X_c, X_sklearn, output_dir='../report'):
    """
    Compara numéricamente los resultados de C y sklearn.
    
    Parameters:
    -----------
    X_c : numpy.ndarray
        Datos proyectados por C
    X_sklearn : numpy.ndarray
        Datos proyectados por sklearn
    output_dir : str
        Directorio para guardar resultados
    """
    print("\n" + "=" * 70)
    print("COMPARACIÓN NUMÉRICA")
    print("=" * 70)
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Los componentes pueden tener signos opuestos (son equivalentes)
    # Verificar ambas posibilidades
    mse_normal = mean_squared_error(X_sklearn, X_c)
    mse_flipped = mean_squared_error(X_sklearn, -X_c)
    
    mae_normal = mean_absolute_error(X_sklearn, X_c)
    mae_flipped = mean_absolute_error(X_sklearn, -X_c)
    
    # Usar la mejor comparación
    if mse_flipped < mse_normal:
        X_c_adjusted = -X_c
        mse = mse_flipped
        mae = mae_flipped
        sign_note = " (con inversión de signo)"
    else:
        X_c_adjusted = X_c
        mse = mse_normal
        mae = mae_normal
        sign_note = ""
    
    # Calcular correlación
    correlations = []
    for i in range(X_c.shape[1]):
        corr = np.corrcoef(X_sklearn[:, i], X_c_adjusted[:, i])[0, 1]
        correlations.append(corr)
    
    # Diferencias
    diff = X_sklearn - X_c_adjusted
    max_diff = np.max(np.abs(diff))
    mean_diff = np.mean(np.abs(diff))
    
    print(f"\nMétricas de comparación{sign_note}:")
    print(f"  - MSE (Error Cuadrático Medio):        {mse:.6e}")
    print(f"  - MAE (Error Absoluto Medio):          {mae:.6e}")
    print(f"  - Diferencia máxima:                   {max_diff:.6e}")
    print(f"  - Diferencia media (abs):              {mean_diff:.6e}")
    print(f"\nCorrelación por componente:")
    for i, corr in enumerate(correlations):
        print(f"  - PC{i+1}: {corr:.6f}")
    
    # Guardar resultados
    with open(output_path / 'numerical_comparison.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("COMPARACIÓN NUMÉRICA: PCA en C vs sklearn\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Forma de los datos:\n")
        f.write(f"  - C output:      {X_c.shape}\n")
        f.write(f"  - sklearn output: {X_sklearn.shape}\n\n")
        
        f.write(f"Métricas de error{sign_note}:\n")
        f.write(f"  - MSE:           {mse:.6e}\n")
        f.write(f"  - MAE:           {mae:.6e}\n")
        f.write(f"  - Max diff:      {max_diff:.6e}\n")
        f.write(f"  - Mean diff:     {mean_diff:.6e}\n\n")
        
        f.write(f"Correlación por componente:\n")
        for i, corr in enumerate(correlations):
            f.write(f"  - PC{i+1}: {corr:.6f}\n")
        
        f.write("\nEstadísticas de diferencias:\n")
        for i in range(X_c.shape[1]):
            diff_comp = X_sklearn[:, i] - X_c_adjusted[:, i]
            f.write(f"\n  PC{i+1}:\n")
            f.write(f"    Media:    {np.mean(diff_comp):.6e}\n")
            f.write(f"    Std:      {np.std(diff_comp):.6e}\n")
            f.write(f"    Min:      {np.min(diff_comp):.6e}\n")
            f.write(f"    Max:      {np.max(diff_comp):.6e}\n")
    
    print(f"\n✓ Resultados numéricos guardados en: {output_path / 'numerical_comparison.txt'}")
    
    return X_c_adjusted, correlations


def plot_comparisons(X_c, X_sklearn, y, output_dir='../report/comparison_plots'):
    """
    Genera gráficas comparativas.
    
    Parameters:
    -----------
    X_c : numpy.ndarray
        Datos proyectados por C (ajustados)
    X_sklearn : numpy.ndarray
        Datos proyectados por sklearn
    y : numpy.ndarray
        Etiquetas
    output_dir : str
        Directorio para guardar gráficas
    """
    print("\n" + "=" * 70)
    print("GENERANDO GRÁFICAS COMPARATIVAS")
    print("=" * 70)
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Scatter plot lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # C implementation
    for class_label in np.unique(y):
        mask = y == class_label
        axes[0].scatter(X_c[mask, 0], X_c[mask, 1], 
                       alpha=0.6, s=30, label=f'Clase {int(class_label)}')
    axes[0].set_xlabel('PC1')
    axes[0].set_ylabel('PC2')
    axes[0].set_title('PCA - Implementación en C')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # sklearn
    for class_label in np.unique(y):
        mask = y == class_label
        axes[1].scatter(X_sklearn[mask, 0], X_sklearn[mask, 1], 
                       alpha=0.6, s=30, label=f'Clase {int(class_label)}')
    axes[1].set_xlabel('PC1')
    axes[1].set_ylabel('PC2')
    axes[1].set_title('PCA - sklearn')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path / 'pca_comparison_scatter.png', dpi=300, bbox_inches='tight')
    print(f"✓ Scatter comparison guardado")
    plt.close()
    
    # 2. Superposición de ambos resultados
    fig, ax = plt.subplots(figsize=(12, 10))
    
    ax.scatter(X_c[:, 0], X_c[:, 1], alpha=0.4, s=40, c='blue', 
              label='C implementation', marker='o')
    ax.scatter(X_sklearn[:, 0], X_sklearn[:, 1], alpha=0.4, s=40, c='red', 
              label='sklearn', marker='x')
    
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_title('Superposición: PCA en C vs sklearn')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path / 'pca_overlay.png', dpi=300, bbox_inches='tight')
    print(f"✓ Overlay plot guardado")
    plt.close()
    
    # 3. Scatter plots por componente
    n_components = X_c.shape[1]
    fig, axes = plt.subplots(1, n_components, figsize=(8*n_components, 6))
    
    if n_components == 1:
        axes = [axes]
    
    for i in range(n_components):
        axes[i].scatter(X_sklearn[:, i], X_c[:, i], alpha=0.5, s=20)
        
        # Línea de referencia perfecta
        min_val = min(X_sklearn[:, i].min(), X_c[:, i].min())
        max_val = max(X_sklearn[:, i].max(), X_c[:, i].max())
        axes[i].plot([min_val, max_val], [min_val, max_val], 
                    'r--', linewidth=2, label='Perfect match')
        
        axes[i].set_xlabel(f'sklearn PC{i+1}')
        axes[i].set_ylabel(f'C PC{i+1}')
        axes[i].set_title(f'Componente Principal {i+1}')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
        axes[i].set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    plt.savefig(output_path / 'pca_component_correlation.png', dpi=300, bbox_inches='tight')
    print(f"✓ Component correlation guardado")
    plt.close()
    
    # 4. Distribuciones de diferencias
    fig, axes = plt.subplots(1, n_components, figsize=(8*n_components, 6))
    
    if n_components == 1:
        axes = [axes]
    
    for i in range(n_components):
        diff = X_sklearn[:, i] - X_c[:, i]
        
        axes[i].hist(diff, bins=50, alpha=0.7, edgecolor='black')
        axes[i].axvline(0, color='red', linestyle='--', linewidth=2, label='Cero')
        axes[i].axvline(np.mean(diff), color='green', linestyle='-', 
                       linewidth=2, label=f'Media: {np.mean(diff):.2e}')
        
        axes[i].set_xlabel('Diferencia (sklearn - C)')
        axes[i].set_ylabel('Frecuencia')
        axes[i].set_title(f'Distribución de Diferencias - PC{i+1}')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path / 'pca_difference_distribution.png', dpi=300, bbox_inches='tight')
    print(f"✓ Difference distribution guardado")
    plt.close()
    
    # 5. Boxplot de errores absolutos
    fig, ax = plt.subplots(figsize=(10, 6))
    
    errors = []
    labels = []
    for i in range(n_components):
        errors.append(np.abs(X_sklearn[:, i] - X_c[:, i]))
        labels.append(f'PC{i+1}')
    
    ax.boxplot(errors, labels=labels)
    ax.set_ylabel('Error Absoluto')
    ax.set_title('Distribución de Errores Absolutos por Componente')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path / 'pca_error_boxplot.png', dpi=300, bbox_inches='tight')
    print(f"✓ Error boxplot guardado")
    plt.close()
    
    print(f"\n✓ Todas las gráficas guardadas en: {output_path}")


def generate_report(X_input, X_c, X_sklearn, y, pca_model, correlations, 
                   output_dir='../report'):
    """
    Genera un reporte completo de la comparación.
    """
    print("\n" + "=" * 70)
    print("GENERANDO REPORTE FINAL")
    print("=" * 70)
    
    output_path = Path(output_dir)
    
    with open(output_path / 'validation_report.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("REPORTE DE VALIDACIÓN - IMPLEMENTACIÓN PCA EN C\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("RESUMEN EJECUTIVO\n")
        f.write("-" * 70 + "\n")
        f.write(f"Este reporte compara la implementación de PCA en C con la\n")
        f.write(f"implementación de referencia de scikit-learn.\n\n")
        
        f.write("DATOS\n")
        f.write("-" * 70 + "\n")
        f.write(f"Dimensiones originales:  {X_input.shape[0]} muestras x {X_input.shape[1]} características\n")
        f.write(f"Dimensiones reducidas:   {X_c.shape[0]} muestras x {X_c.shape[1]} componentes\n")
        f.write(f"Reducción dimensional:   {(1 - X_c.shape[1]/X_input.shape[1])*100:.1f}%\n")
        f.write(f"Número de clases:        {len(np.unique(y))}\n\n")
        
        f.write("VARIANZA EXPLICADA\n")
        f.write("-" * 70 + "\n")
        f.write(f"sklearn:\n")
        for i, var in enumerate(pca_model.explained_variance_ratio_):
            f.write(f"  PC{i+1}: {var*100:.2f}%\n")
        f.write(f"  Total: {pca_model.explained_variance_ratio_.sum()*100:.2f}%\n\n")
        
        f.write("VALIDACIÓN\n")
        f.write("-" * 70 + "\n")
        f.write(f"Correlación entre implementaciones:\n")
        for i, corr in enumerate(correlations):
            f.write(f"  PC{i+1}: {corr:.6f}\n")
        f.write(f"\nInterpretación:\n")
        f.write(f"  - Correlación > 0.99:  Excelente concordancia\n")
        f.write(f"  - Correlación > 0.95:  Buena concordancia\n")
        f.write(f"  - Correlación < 0.95:  Revisar implementación\n\n")
        
        avg_corr = np.mean(correlations)
        if avg_corr > 0.99:
            status = "EXCELENTE ✓"
        elif avg_corr > 0.95:
            status = "BUENA ✓"
        else:
            status = "REVISAR ⚠"
        
        f.write(f"CONCLUSIÓN\n")
        f.write("-" * 70 + "\n")
        f.write(f"Estado de la implementación: {status}\n")
        f.write(f"Correlación promedio: {avg_corr:.6f}\n\n")
        
        f.write(f"La implementación en C {'produce resultados' if avg_corr > 0.99 else 'requiere revisión'}\n")
        f.write(f"{'prácticamente idénticos' if avg_corr > 0.99 else 'similares'} a sklearn.\n\n")
        
        f.write("ARCHIVOS GENERADOS\n")
        f.write("-" * 70 + "\n")
        f.write("  - numerical_comparison.txt: Métricas numéricas detalladas\n")
        f.write("  - pca_comparison_scatter.png: Comparación lado a lado\n")
        f.write("  - pca_overlay.png: Superposición de resultados\n")
        f.write("  - pca_component_correlation.png: Correlación por componente\n")
        f.write("  - pca_difference_distribution.png: Distribución de diferencias\n")
        f.write("  - pca_error_boxplot.png: Boxplot de errores\n")
        f.write("\n")
    
    print(f"✓ Reporte final guardado en: {output_path / 'validation_report.txt'}")


def main():
    """Función principal."""
    print("\n" + "=" * 70)
    print(" " * 15 + "VALIDACIÓN DE PCA EN C")
    print("=" * 70)
    print()
    
    try:
        # 1. Cargar datos
        X_input, X_c, y = load_data()
        
        # 2. Aplicar PCA con sklearn
        X_sklearn, pca_model = apply_sklearn_pca(X_input, n_components=X_c.shape[1])
        
        # 3. Comparación numérica
        X_c_adjusted, correlations = compare_numerical(X_c, X_sklearn)
        
        # 4. Generar gráficas
        plot_comparisons(X_c_adjusted, X_sklearn, y)
        
        # 5. Generar reporte
        generate_report(X_input, X_c_adjusted, X_sklearn, y, pca_model, correlations)
        
        print("\n" + "=" * 70)
        print("✓ VALIDACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 70)
        print("\nRevisa los archivos generados en:")
        print("  - report/numerical_comparison.txt")
        print("  - report/validation_report.txt")
        print("  - report/comparison_plots/")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
