/*
 * pca.h - Header file for PCA implementation
 * 
 * This file contains declarations for the PCA algorithm implementation.
 * The algorithm follows these steps:
 *   1. Read data from CSV file
 *   2. Center the data (subtract mean)
 *   3. Compute covariance matrix
 *   4. Compute eigenvectors and eigenvalues
 *   5. Sort eigenvectors by eigenvalues (descending)
 *   6. Project data onto K principal components
 *   7. Write results to CSV file
 * 
 * Author: PCA Lab
 * Date: October 2025
 */

#ifndef PCA_H
#define PCA_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* Configuration constants */
#define MAX_LINE_LENGTH 4096
#define MAX_FILENAME_LENGTH 256

/* Matrix structure */
typedef struct {
    double **data;      /* 2D array of data */
    int rows;          /* Number of rows (samples) */
    int cols;          /* Number of columns (features) */
} Matrix;

/* PCA configuration structure */
typedef struct {
    int n_components;           /* Number of principal components (K) */
    double *mean;              /* Mean of each feature */
    double *eigenvalues;       /* Eigenvalues */
    Matrix *eigenvectors;      /* Eigenvectors (components) */
    double explained_variance_ratio;  /* Variance explained */
} PCAModel;

/* ============================================
 * Matrix Operations
 * ============================================ */

/**
 * Create a new matrix with given dimensions
 * @param rows Number of rows
 * @param cols Number of columns
 * @return Pointer to newly created matrix, NULL on failure
 */
Matrix* matrix_create(int rows, int cols);

/**
 * Free memory allocated for a matrix
 * @param mat Matrix to free
 */
void matrix_free(Matrix *mat);

/**
 * Copy matrix data
 * @param dest Destination matrix
 * @param src Source matrix
 */
void matrix_copy(Matrix *dest, const Matrix *src);

/**
 * Print matrix (for debugging)
 * @param mat Matrix to print
 * @param name Name of the matrix
 */
void matrix_print(const Matrix *mat, const char *name);

/**
 * Matrix multiplication: C = A * B
 * @param A First matrix
 * @param B Second matrix
 * @return Result matrix C
 */
Matrix* matrix_multiply(const Matrix *A, const Matrix *B);

/**
 * Transpose a matrix
 * @param mat Input matrix
 * @return Transposed matrix
 */
Matrix* matrix_transpose(const Matrix *mat);

/* ============================================
 * File I/O Operations
 * ============================================ */

/**
 * Read CSV file into matrix
 * @param filename Path to CSV file
 * @return Matrix containing the data, NULL on failure
 */
Matrix* read_csv(const char *filename);

/**
 * Write matrix to CSV file
 * @param mat Matrix to write
 * @param filename Output filename
 * @return 0 on success, -1 on failure
 */
int write_csv(const Matrix *mat, const char *filename);

/**
 * Count rows and columns in CSV file
 * @param filename Path to CSV file
 * @param rows Pointer to store row count
 * @param cols Pointer to store column count
 * @return 0 on success, -1 on failure
 */
int get_csv_dimensions(const char *filename, int *rows, int *cols);

/* ============================================
 * Statistical Operations
 * ============================================ */

/**
 * Compute mean of each column
 * @param mat Input matrix
 * @return Array of means (size = mat->cols)
 */
double* compute_mean(const Matrix *mat);

/**
 * Center the data by subtracting mean from each column
 * @param mat Input matrix (will be modified in-place)
 * @param mean Array of means for each column
 */
void center_data(Matrix *mat, const double *mean);

/**
 * Compute covariance matrix
 * @param mat Input matrix (should be centered)
 * @return Covariance matrix (cols x cols)
 */
Matrix* compute_covariance(const Matrix *mat);

/* ============================================
 * PCA Core Algorithm
 * ============================================ */

/**
 * Compute eigenvalues and eigenvectors using Power Iteration method
 * @param cov_matrix Covariance matrix
 * @param eigenvalues Output array for eigenvalues
 * @param eigenvectors Output matrix for eigenvectors
 * @param max_iterations Maximum iterations for convergence
 * @param tolerance Convergence tolerance
 * @return 0 on success, -1 on failure
 */
int compute_eigen(const Matrix *cov_matrix, double *eigenvalues, 
                 Matrix *eigenvectors, int max_iterations, double tolerance);

/**
 * Sort eigenvalues and eigenvectors in descending order
 * @param eigenvalues Array of eigenvalues
 * @param eigenvectors Matrix of eigenvectors
 * @param n Number of eigenvalues/eigenvectors
 */
void sort_eigen(double *eigenvalues, Matrix *eigenvectors, int n);

/**
 * Project data onto principal components
 * @param data Input data (centered)
 * @param eigenvectors Principal components
 * @param k Number of components to use
 * @return Projected data (rows x k)
 */
Matrix* project_data(const Matrix *data, const Matrix *eigenvectors, int k);

/**
 * Create and train PCA model
 * @param data Input data matrix
 * @param n_components Number of principal components
 * @return Trained PCA model
 */
PCAModel* pca_fit(Matrix *data, int n_components);

/**
 * Transform data using fitted PCA model
 * @param model Fitted PCA model
 * @param data Input data
 * @return Transformed data
 */
Matrix* pca_transform(const PCAModel *model, Matrix *data);

/**
 * Free PCA model memory
 * @param model PCA model to free
 */
void pca_free(PCAModel *model);

/* ============================================
 * Utility Functions
 * ============================================ */

/**
 * Compute L2 norm of a vector
 * @param vec Vector
 * @param size Size of vector
 * @return L2 norm
 */
double vector_norm(const double *vec, int size);

/**
 * Normalize a vector to unit length
 * @param vec Vector to normalize (modified in-place)
 * @param size Size of vector
 */
void vector_normalize(double *vec, int size);

/**
 * Dot product of two vectors
 * @param vec1 First vector
 * @param vec2 Second vector
 * @param size Size of vectors
 * @return Dot product
 */
double vector_dot(const double *vec1, const double *vec2, int size);

/**
 * Print progress information
 * @param message Progress message
 */
void print_progress(const char *message);

/**
 * Print error message
 * @param message Error message
 */
void print_error(const char *message);

#endif /* PCA_H */
