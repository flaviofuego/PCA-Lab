/*
 * main.c - Main program for PCA implementation
 * 
 * This program reads data from a CSV file, applies PCA dimensionality
 * reduction, and writes the transformed data to an output CSV file.
 * 
 * Usage: ./pca_program [input_file] [output_file] [n_components] [timestamp]
 * 
 * Default values:
 *   input_file: data/input_data.csv
 *   output_file: data/output_data.csv
 *   n_components: 2
 *   timestamp: (none)
 * 
 * Author: PCA Lab
 * Date: October 2025
 */

#include "pca.h"
#include <time.h>

/* Default configuration */
#define DEFAULT_INPUT_FILE  "data/input_data.csv"
#define DEFAULT_OUTPUT_FILE "data/output_data.csv"
#define DEFAULT_K_COMPONENTS 2

void print_usage(const char *program_name) {
    printf("\nUsage: %s [input_file] [output_file] [n_components] [timestamp]\n", program_name);
    printf("\nArguments:\n");
    printf("  input_file    : Path to input CSV file (default: %s)\n", DEFAULT_INPUT_FILE);
    printf("  output_file   : Path to output CSV file (default: %s)\n", DEFAULT_OUTPUT_FILE);
    printf("  n_components  : Number of principal components (default: %d)\n", DEFAULT_K_COMPONENTS);
    printf("  timestamp     : Optional timestamp string to append to output filename\n");
    printf("\nExamples:\n");
    printf("  %s data/input_data.csv data/output_data.csv 3\n", program_name);
    printf("  %s data/input_data.csv data/output_data.csv 2 20241018_143025\n", program_name);
    printf("\n");
}

void generate_timestamped_filename(const char *original_filename, const char *timestamp, char *output_filename) {
    /* Extract directory, base name, and extension */
    char *last_slash = strrchr(original_filename, '/');
    char *last_dot = strrchr(original_filename, '.');
    
    if (last_slash && last_dot && last_dot > last_slash) {
        /* Has directory and extension */
        int dir_len = last_slash - original_filename + 1;
        int base_len = last_dot - last_slash - 1;
        
        strncpy(output_filename, original_filename, dir_len);
        output_filename[dir_len] = '\0';
        
        strncat(output_filename, last_slash + 1, base_len);
        strcat(output_filename, "_");
        strcat(output_filename, timestamp);
        strcat(output_filename, last_dot);
    } else if (last_dot) {
        /* Has extension but no directory */
        int base_len = last_dot - original_filename;
        
        strncpy(output_filename, original_filename, base_len);
        output_filename[base_len] = '\0';
        
        strcat(output_filename, "_");
        strcat(output_filename, timestamp);
        strcat(output_filename, last_dot);
    } else {
        /* No extension */
        strcpy(output_filename, original_filename);
        strcat(output_filename, "_");
        strcat(output_filename, timestamp);
    }
}

void copy_file(const char *source, const char *destination) {
    FILE *src = fopen(source, "r");
    FILE *dst = fopen(destination, "w");
    
    if (src && dst) {
        int c;
        while ((c = fgetc(src)) != EOF) {
            fputc(c, dst);
        }
    }
    
    if (src) fclose(src);
    if (dst) fclose(dst);
}

int main(int argc, char *argv[]) {
    /* Configuration */
    char input_file[MAX_FILENAME_LENGTH] = DEFAULT_INPUT_FILE;
    char output_file[MAX_FILENAME_LENGTH] = DEFAULT_OUTPUT_FILE;
    char timestamped_output_file[MAX_FILENAME_LENGTH];
    char *timestamp = NULL;
    int n_components = DEFAULT_K_COMPONENTS;
    int use_timestamp = 0;
    
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
    
    if (argc > 4) {
        timestamp = argv[4];
        use_timestamp = 1;
        generate_timestamped_filename(output_file, timestamp, timestamped_output_file);
    } else {
        strcpy(timestamped_output_file, output_file);
    }
    
    /* Print configuration */
    printf("Configuration:\n");
    printf("  Input file:       %s\n", input_file);
    if (use_timestamp) {
        printf("  Output file:      %s (timestamped: %s)\n", output_file, timestamped_output_file);
        printf("  Timestamp:        %s\n", timestamp);
    } else {
        printf("  Output file:      %s\n", output_file);
    }
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
    
    if (write_csv(transformed, timestamped_output_file) != 0) {
        print_error("Failed to write output file");
        matrix_free(transformed);
        pca_free(model);
        matrix_free(data);
        return 1;
    }
    
    /* If using timestamp, also create/update the "latest" version */
    if (use_timestamp && strcmp(timestamped_output_file, output_file) != 0) {
        printf("Creating link to latest version: %s\n", output_file);
        copy_file(timestamped_output_file, output_file);
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
    if (use_timestamp) {
        printf("\nOutput saved to: %s\n", timestamped_output_file);
        printf("Latest version:   %s\n", output_file);
    } else {
        printf("\nOutput saved to: %s\n", output_file);
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
