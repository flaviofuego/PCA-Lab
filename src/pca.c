/*
 * pca.c - Implementation of PCA algorithm
 * 
 * This file contains the implementation of the PCA algorithm and
 * supporting functions for matrix operations, file I/O, and
 * statistical computations.
 * 
 * Author: PCA Lab
 * Date: October 2025
 */

#include "pca.h"

/* ============================================
 * Matrix Operations Implementation
 * ============================================ */

Matrix* matrix_create(int rows, int cols) {
    if (rows <= 0 || cols <= 0) {
        print_error("Invalid matrix dimensions");
        return NULL;
    }
    
    Matrix *mat = (Matrix*)malloc(sizeof(Matrix));
    if (!mat) {
        print_error("Failed to allocate matrix structure");
        return NULL;
    }
    
    mat->rows = rows;
    mat->cols = cols;
    
    /* Allocate array of row pointers */
    mat->data = (double**)malloc(rows * sizeof(double*));
    if (!mat->data) {
        print_error("Failed to allocate matrix rows");
        free(mat);
        return NULL;
    }
    
    /* Allocate each row */
    for (int i = 0; i < rows; i++) {
        mat->data[i] = (double*)calloc(cols, sizeof(double));
        if (!mat->data[i]) {
            /* Free previously allocated rows */
            for (int j = 0; j < i; j++) {
                free(mat->data[j]);
            }
            free(mat->data);
            free(mat);
            print_error("Failed to allocate matrix row");
            return NULL;
        }
    }
    
    return mat;
}

void matrix_free(Matrix *mat) {
    if (!mat) return;
    
    if (mat->data) {
        for (int i = 0; i < mat->rows; i++) {
            if (mat->data[i]) {
                free(mat->data[i]);
            }
        }
        free(mat->data);
    }
    free(mat);
}

void matrix_copy(Matrix *dest, const Matrix *src) {
    if (!dest || !src || dest->rows != src->rows || dest->cols != src->cols) {
        print_error("Invalid matrix copy operation");
        return;
    }
    
    for (int i = 0; i < src->rows; i++) {
        for (int j = 0; j < src->cols; j++) {
            dest->data[i][j] = src->data[i][j];
        }
    }
}

void matrix_print(const Matrix *mat, const char *name) {
    if (!mat) return;
    
    printf("\n%s (%d x %d):\n", name, mat->rows, mat->cols);
    
    int max_rows = (mat->rows > 5) ? 5 : mat->rows;
    int max_cols = (mat->cols > 5) ? 5 : mat->cols;
    
    for (int i = 0; i < max_rows; i++) {
        for (int j = 0; j < max_cols; j++) {
            printf("%10.6f ", mat->data[i][j]);
        }
        if (mat->cols > 5) printf("...");
        printf("\n");
    }
    if (mat->rows > 5) printf("...\n");
    printf("\n");
}

Matrix* matrix_multiply(const Matrix *A, const Matrix *B) {
    if (!A || !B || A->cols != B->rows) {
        print_error("Invalid matrix multiplication dimensions");
        return NULL;
    }
    
    Matrix *C = matrix_create(A->rows, B->cols);
    if (!C) return NULL;
    
    for (int i = 0; i < A->rows; i++) {
        for (int j = 0; j < B->cols; j++) {
            double sum = 0.0;
            for (int k = 0; k < A->cols; k++) {
                sum += A->data[i][k] * B->data[k][j];
            }
            C->data[i][j] = sum;
        }
    }
    
    return C;
}

Matrix* matrix_transpose(const Matrix *mat) {
    if (!mat) return NULL;
    
    Matrix *trans = matrix_create(mat->cols, mat->rows);
    if (!trans) return NULL;
    
    for (int i = 0; i < mat->rows; i++) {
        for (int j = 0; j < mat->cols; j++) {
            trans->data[j][i] = mat->data[i][j];
        }
    }
    
    return trans;
}

/* ============================================
 * File I/O Operations Implementation
 * ============================================ */

int get_csv_dimensions(const char *filename, int *rows, int *cols) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        print_error("Failed to open file for reading");
        return -1;
    }
    
    char line[MAX_LINE_LENGTH];
    *rows = 0;
    *cols = 0;
    
    /* Count rows and columns */
    while (fgets(line, sizeof(line), file)) {
        (*rows)++;
        
        /* Count columns in first row */
        if (*rows == 1) {
            char *token = strtok(line, ",");
            while (token != NULL) {
                (*cols)++;
                token = strtok(NULL, ",");
            }
        }
    }
    
    fclose(file);
    return 0;
}

Matrix* read_csv(const char *filename) {
    int rows, cols;
    
    print_progress("Reading CSV file...");
    
    /* Get dimensions */
    if (get_csv_dimensions(filename, &rows, &cols) != 0) {
        return NULL;
    }
    
    printf("  Detected %d rows x %d columns\n", rows, cols);
    
    /* Create matrix */
    Matrix *mat = matrix_create(rows, cols);
    if (!mat) return NULL;
    
    /* Open file again to read data */
    FILE *file = fopen(filename, "r");
    if (!file) {
        matrix_free(mat);
        print_error("Failed to open file for reading");
        return NULL;
    }
    
    char line[MAX_LINE_LENGTH];
    int row = 0;
    
    while (fgets(line, sizeof(line), file) && row < rows) {
        int col = 0;
        char *token = strtok(line, ",");
        
        while (token != NULL && col < cols) {
            mat->data[row][col] = atof(token);
            col++;
            token = strtok(NULL, ",");
        }
        row++;
    }
    
    fclose(file);
    print_progress("CSV file loaded successfully");
    
    return mat;
}

int write_csv(const Matrix *mat, const char *filename) {
    if (!mat || !filename) return -1;
    
    print_progress("Writing results to CSV...");
    
    FILE *file = fopen(filename, "w");
    if (!file) {
        print_error("Failed to open file for writing");
        return -1;
    }
    
    for (int i = 0; i < mat->rows; i++) {
        for (int j = 0; j < mat->cols; j++) {
            fprintf(file, "%.6f", mat->data[i][j]);
            if (j < mat->cols - 1) {
                fprintf(file, ",");
            }
        }
        fprintf(file, "\n");
    }
    
    fclose(file);
    printf("  Wrote %d rows x %d columns to %s\n", mat->rows, mat->cols, filename);
    
    return 0;
}

/* ============================================
 * Statistical Operations Implementation
 * ============================================ */

double* compute_mean(const Matrix *mat) {
    if (!mat) return NULL;
    
    double *mean = (double*)calloc(mat->cols, sizeof(double));
    if (!mean) {
        print_error("Failed to allocate mean array");
        return NULL;
    }
    
    /* Sum each column */
    for (int j = 0; j < mat->cols; j++) {
        for (int i = 0; i < mat->rows; i++) {
            mean[j] += mat->data[i][j];
        }
        mean[j] /= mat->rows;
    }
    
    return mean;
}

void center_data(Matrix *mat, const double *mean) {
    if (!mat || !mean) return;
    
    print_progress("Centering data (subtracting mean)...");
    
    for (int i = 0; i < mat->rows; i++) {
        for (int j = 0; j < mat->cols; j++) {
            mat->data[i][j] -= mean[j];
        }
    }
}

Matrix* compute_covariance(const Matrix *mat) {
    if (!mat) return NULL;
    
    print_progress("Computing covariance matrix...");
    
    /* Covariance = (X^T * X) / (n - 1) */
    Matrix *X_T = matrix_transpose(mat);
    if (!X_T) return NULL;
    
    Matrix *cov = matrix_multiply(X_T, mat);
    matrix_free(X_T);
    
    if (!cov) return NULL;
    
    /* Divide by (n - 1) */
    double divisor = (mat->rows > 1) ? (mat->rows - 1) : 1;
    for (int i = 0; i < cov->rows; i++) {
        for (int j = 0; j < cov->cols; j++) {
            cov->data[i][j] /= divisor;
        }
    }
    
    printf("  Covariance matrix: %d x %d\n", cov->rows, cov->cols);
    
    return cov;
}

/* ============================================
 * PCA Core Algorithm Implementation
 * ============================================ */

int compute_eigen(const Matrix *cov_matrix, double *eigenvalues, 
                 Matrix *eigenvectors, int max_iterations, double tolerance) {
    if (!cov_matrix || !eigenvalues || !eigenvectors) return -1;
    
    print_progress("Computing eigenvalues and eigenvectors...");
    
    int n = cov_matrix->rows;
    Matrix *A = matrix_create(n, n);
    if (!A) return -1;
    
    /* Copy covariance matrix (we'll deflate it) */
    matrix_copy(A, cov_matrix);
    
    /* Power iteration for each eigenvector */
    for (int k = 0; k < n; k++) {
        double *v = (double*)malloc(n * sizeof(double));
        if (!v) {
            matrix_free(A);
            return -1;
        }
        
        /* Initialize with random values */
        for (int i = 0; i < n; i++) {
            v[i] = 1.0 / sqrt(n);
        }
        
        /* Power iteration */
        double lambda = 0.0;
        for (int iter = 0; iter < max_iterations; iter++) {
            /* v_new = A * v */
            double *v_new = (double*)calloc(n, sizeof(double));
            if (!v_new) {
                free(v);
                matrix_free(A);
                return -1;
            }
            
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    v_new[i] += A->data[i][j] * v[j];
                }
            }
            
            /* Compute eigenvalue (Rayleigh quotient) */
            double lambda_new = 0.0;
            for (int i = 0; i < n; i++) {
                lambda_new += v_new[i] * v[i];
            }
            
            /* Normalize */
            vector_normalize(v_new, n);
            
            /* Check convergence */
            if (fabs(lambda_new - lambda) < tolerance) {
                lambda = lambda_new;
                memcpy(v, v_new, n * sizeof(double));
                free(v_new);
                break;
            }
            
            lambda = lambda_new;
            memcpy(v, v_new, n * sizeof(double));
            free(v_new);
        }
        
        /* Store eigenvalue and eigenvector */
        eigenvalues[k] = lambda;
        for (int i = 0; i < n; i++) {
            eigenvectors->data[i][k] = v[i];
        }
        
        /* Deflate matrix: A = A - lambda * v * v^T */
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                A->data[i][j] -= lambda * v[i] * v[j];
            }
        }
        
        free(v);
    }
    
    matrix_free(A);
    
    printf("  Computed %d eigenvalues\n", n);
    
    return 0;
}

void sort_eigen(double *eigenvalues, Matrix *eigenvectors, int n) {
    /* Simple bubble sort (sufficient for small n) */
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (eigenvalues[j] < eigenvalues[j + 1]) {
                /* Swap eigenvalues */
                double temp = eigenvalues[j];
                eigenvalues[j] = eigenvalues[j + 1];
                eigenvalues[j + 1] = temp;
                
                /* Swap eigenvectors */
                for (int k = 0; k < eigenvectors->rows; k++) {
                    temp = eigenvectors->data[k][j];
                    eigenvectors->data[k][j] = eigenvectors->data[k][j + 1];
                    eigenvectors->data[k][j + 1] = temp;
                }
            }
        }
    }
}

Matrix* project_data(const Matrix *data, const Matrix *eigenvectors, int k) {
    if (!data || !eigenvectors || k <= 0) return NULL;
    
    print_progress("Projecting data onto principal components...");
    
    /* Create matrix with first k eigenvectors */
    Matrix *components = matrix_create(eigenvectors->rows, k);
    if (!components) return NULL;
    
    for (int i = 0; i < eigenvectors->rows; i++) {
        for (int j = 0; j < k; j++) {
            components->data[i][j] = eigenvectors->data[i][j];
        }
    }
    
    /* Project: X_pca = X * components */
    Matrix *projected = matrix_multiply(data, components);
    matrix_free(components);
    
    if (projected) {
        printf("  Projected to %d dimensions\n", k);
    }
    
    return projected;
}

PCAModel* pca_fit(Matrix *data, int n_components) {
    if (!data || n_components <= 0 || n_components > data->cols) {
        print_error("Invalid PCA parameters");
        return NULL;
    }
    
    printf("\n========================================\n");
    printf("Training PCA Model\n");
    printf("========================================\n");
    printf("Input shape: %d samples x %d features\n", data->rows, data->cols);
    printf("Target components: %d\n", n_components);
    printf("\n");
    
    /* Allocate PCA model */
    PCAModel *model = (PCAModel*)malloc(sizeof(PCAModel));
    if (!model) {
        print_error("Failed to allocate PCA model");
        return NULL;
    }
    
    model->n_components = n_components;
    
    /* Step 1: Compute mean */
    model->mean = compute_mean(data);
    if (!model->mean) {
        free(model);
        return NULL;
    }
    
    /* Step 2: Center data */
    center_data(data, model->mean);
    
    /* Step 3: Compute covariance matrix */
    Matrix *cov = compute_covariance(data);
    if (!cov) {
        free(model->mean);
        free(model);
        return NULL;
    }
    
    /* Step 4: Compute eigenvalues and eigenvectors */
    model->eigenvalues = (double*)malloc(data->cols * sizeof(double));
    model->eigenvectors = matrix_create(data->cols, data->cols);
    
    if (!model->eigenvalues || !model->eigenvectors) {
        matrix_free(cov);
        free(model->mean);
        if (model->eigenvalues) free(model->eigenvalues);
        if (model->eigenvectors) matrix_free(model->eigenvectors);
        free(model);
        return NULL;
    }
    
    int result = compute_eigen(cov, model->eigenvalues, model->eigenvectors, 
                               1000, 1e-10);
    matrix_free(cov);
    
    if (result != 0) {
        pca_free(model);
        return NULL;
    }
    
    /* Step 5: Sort eigenvalues and eigenvectors */
    print_progress("Sorting by eigenvalues (descending)...");
    sort_eigen(model->eigenvalues, model->eigenvectors, data->cols);
    
    /* Calculate explained variance */
    double total_variance = 0.0;
    double explained_variance = 0.0;
    
    for (int i = 0; i < data->cols; i++) {
        total_variance += model->eigenvalues[i];
        if (i < n_components) {
            explained_variance += model->eigenvalues[i];
        }
    }
    
    model->explained_variance_ratio = explained_variance / total_variance;
    
    printf("\n========================================\n");
    printf("PCA Model Training Complete\n");
    printf("========================================\n");
    printf("Explained variance ratio: %.4f (%.2f%%)\n", 
           model->explained_variance_ratio, 
           model->explained_variance_ratio * 100);
    printf("\nTop eigenvalues:\n");
    for (int i = 0; i < (n_components < 5 ? n_components : 5); i++) {
        printf("  PC%d: %.6f\n", i + 1, model->eigenvalues[i]);
    }
    printf("\n");
    
    return model;
}

Matrix* pca_transform(const PCAModel *model, Matrix *data) {
    if (!model || !data) return NULL;
    
    /* Center data using stored mean */
    center_data(data, model->mean);
    
    /* Project onto principal components */
    return project_data(data, model->eigenvectors, model->n_components);
}

void pca_free(PCAModel *model) {
    if (!model) return;
    
    if (model->mean) free(model->mean);
    if (model->eigenvalues) free(model->eigenvalues);
    if (model->eigenvectors) matrix_free(model->eigenvectors);
    free(model);
}

/* ============================================
 * Utility Functions Implementation
 * ============================================ */

double vector_norm(const double *vec, int size) {
    double sum = 0.0;
    for (int i = 0; i < size; i++) {
        sum += vec[i] * vec[i];
    }
    return sqrt(sum);
}

void vector_normalize(double *vec, int size) {
    double norm = vector_norm(vec, size);
    if (norm > 1e-10) {
        for (int i = 0; i < size; i++) {
            vec[i] /= norm;
        }
    }
}

double vector_dot(const double *vec1, const double *vec2, int size) {
    double sum = 0.0;
    for (int i = 0; i < size; i++) {
        sum += vec1[i] * vec2[i];
    }
    return sum;
}

void print_progress(const char *message) {
    printf(">>> %s\n", message);
}

void print_error(const char *message) {
    fprintf(stderr, "ERROR: %s\n", message);
}
