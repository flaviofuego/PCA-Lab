/*
 * main.c - Main program for PCA implementation
 * 
 * This program reads data from a CSV file, applies PCA dimensionality
 * reduction, and writes the transformed data to an output CSV file.
 * 
 * Usage: ./pca_program [input_file] [output_file] [n_components]
 * 
 * Default values:
 *   input_file: data/input_data.csv
 *   output_file: data/output_data.csv
 *   n_components: 2
 * 
 * Author: PCA Lab
 * Date: October 2025
 */

#include "pca.h"

/* Default configuration */
#define DEFAULT_INPUT_FILE  "data/input_data.csv"
#define DEFAULT_OUTPUT_FILE "data/output_data.csv"
#define DEFAULT_K_COMPONENTS 2

void print_usage(const char *program_name) {
    printf("\nUsage: %s [input_file] [output_file] [n_components]\n", program_name);
    printf("\nArguments:\n");
    printf("  input_file    : Path to input CSV file (default: %s)\n", DEFAULT_INPUT_FILE);
    printf("  output_file   : Path to output CSV file (default: %s)\n", DEFAULT_OUTPUT_FILE);
    printf("  n_components  : Number of principal components (default: %d)\n", DEFAULT_K_COMPONENTS);
    printf("\nExample:\n");
    printf("  %s data/input_data.csv data/output_data.csv 3\n", program_name);
    printf("\n");
}

int main(int argc, char *argv[]) {
    /* Configuration */
    char input_file[MAX_FILENAME_LENGTH] = DEFAULT_INPUT_FILE;
    char output_file[MAX_FILENAME_LENGTH] = DEFAULT_OUTPUT_FILE;
    int n_components = DEFAULT_K_COMPONENTS;
    
    /* Banner */
    printf("\n");
    printf("========================================\n");
    printf("  PCA Implementation in C\n");
    printf("  Principal Component Analysis\n");
    printf("========================================\n");
    printf("\n");
    
    /* Parse command line arguments */
    if (argc > 1) {
        if (strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "--help") == 0) {
            print_usage(argv[0]);
            return 0;
        }
        strncpy(input_file, argv[1], MAX_FILENAME_LENGTH - 1);
    }
    
    if (argc > 2) {
        strncpy(output_file, argv[2], MAX_FILENAME_LENGTH - 1);
    }
    
    if (argc > 3) {
        n_components = atoi(argv[3]);
        if (n_components <= 0) {
            print_error("Number of components must be positive");
            return 1;
        }
    }
    
    /* Print configuration */
    printf("Configuration:\n");
    printf("  Input file:       %s\n", input_file);
    printf("  Output file:      %s\n", output_file);
    printf("  Components (K):   %d\n", n_components);
    printf("\n");
    
    /* Step 1: Read input data */
    printf("========================================\n");
    printf("Step 1: Loading Data\n");
    printf("========================================\n");
    
    Matrix *data = read_csv(input_file);
    if (!data) {
        print_error("Failed to read input file");
        return 1;
    }
    
    printf("Data loaded: %d samples x %d features\n", data->rows, data->cols);
    
    /* Validate n_components */
    if (n_components > data->cols) {
        printf("WARNING: n_components (%d) > n_features (%d)\n", 
               n_components, data->cols);
        printf("Setting n_components = %d\n", data->cols);
        n_components = data->cols;
    }
    
    /* Step 2: Fit PCA model */
    printf("\n========================================\n");
    printf("Step 2: Fitting PCA Model\n");
    printf("========================================\n\n");
    
    PCAModel *model = pca_fit(data, n_components);
    if (!model) {
        print_error("Failed to fit PCA model");
        matrix_free(data);
        return 1;
    }
    
    /* Step 3: Transform data */
    printf("========================================\n");
    printf("Step 3: Transforming Data\n");
    printf("========================================\n\n");
    
    /* Re-read data (pca_fit modifies it by centering) */
    Matrix *data_original = read_csv(input_file);
    if (!data_original) {
        print_error("Failed to re-read input file");
        pca_free(model);
        matrix_free(data);
        return 1;
    }
    
    Matrix *transformed = pca_transform(model, data_original);
    matrix_free(data_original);
    
    if (!transformed) {
        print_error("Failed to transform data");
        pca_free(model);
        matrix_free(data);
        return 1;
    }
    
    printf("Transformation complete: %d samples x %d components\n", 
           transformed->rows, transformed->cols);
    
    /* Step 4: Write output */
    printf("\n========================================\n");
    printf("Step 4: Writing Results\n");
    printf("========================================\n\n");
    
    if (write_csv(transformed, output_file) != 0) {
        print_error("Failed to write output file");
        matrix_free(transformed);
        pca_free(model);
        matrix_free(data);
        return 1;
    }
    
    /* Summary statistics */
    printf("\n========================================\n");
    printf("Summary\n");
    printf("========================================\n");
    printf("Original dimensions:      %d x %d\n", data->rows, data->cols);
    printf("Reduced dimensions:       %d x %d\n", transformed->rows, transformed->cols);
    printf("Dimensionality reduction: %.1f%%\n", 
           (1.0 - (double)n_components / data->cols) * 100);
    printf("Variance explained:       %.2f%%\n", 
           model->explained_variance_ratio * 100);
    printf("\nOutput saved to: %s\n", output_file);
    
    /* Print first few transformed samples (for verification) */
    printf("\nFirst 5 transformed samples:\n");
    int max_samples = (transformed->rows < 5) ? transformed->rows : 5;
    for (int i = 0; i < max_samples; i++) {
        printf("Sample %d: [", i + 1);
        for (int j = 0; j < transformed->cols; j++) {
            printf("%.6f", transformed->data[i][j]);
            if (j < transformed->cols - 1) printf(", ");
        }
        printf("]\n");
    }
    
    printf("\n========================================\n");
    printf("PCA Completed Successfully!\n");
    printf("========================================\n\n");
    
    /* Cleanup */
    matrix_free(data);
    matrix_free(transformed);
    pca_free(model);
    
    return 0;
}
