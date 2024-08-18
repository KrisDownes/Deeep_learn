#include <stdio.h>
#include <stdlib.h>

#define N 3

void matmul(int A[][N], int B[][N], int C[][N]){
    for (int i=0; i < N; i++){
        for (int j=0; j < N; j++){
            C[i][j] =0;
            for (int k=0; k < N; k++){
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}
void printMatrix(int matrix[][N]){
    for (int i = 0;i < N; i++){
        for (int j = 0; j < N; j++){
            printf("%d ",matrix[i][j]);
        }
        printf("\n");
    }
}
int main(){
    int A[N][N] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int B[N][N] = {{9, 8, 7}, {6, 5, 4}, {3, 2, 1}};
    int C[N][N];

    printf("Matrix A:\n");
    printMatrix(A);

    printf("Matrix B: \n");
    printMatrix(B);

    matmul(A,B,C);

    printf("Matrix C = A*B \n");
    printMatrix(C);
    return 0;
}