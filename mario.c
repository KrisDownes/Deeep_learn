#include <stdio.h>
#include <stdlib.h>

void brick(int n1) {
    for (int i = 0; i < n1; i++) {
        // Print the left side
        for (int j = 0; j < n1 - i - 1; j++) {
            printf(" ");
        }
        for (int j = 0; j < i + 1; j++) {
            printf("#");
        }
        printf("  ");
        // Print the right side
        for (int j = 0; j < i + 1; j++) {
            printf("#");
        }
        printf("\n");
    }
}


int main(void){
    int n;
    printf("Height: ");
    if (scanf("%d",&n) != 1){
        return 1;
    }
    brick(n);
    return 0;
}