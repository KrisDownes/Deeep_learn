#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>
#include <string.h>


bool is_numeric(const char *str){
    for (size_t i = 0; str[i] != '\0'; i++){
        if (!isdigit(str[i])){
            return false;
        }
    }
    return true;
}

bool luhn(const char *str){
    int sum = 0;
    bool double_next = false;

    for (int i = strlen(str) - 1; i >= 0; i--){
        int digit = str[i] - '0';

        if (double_next){
            digit *=2;
            if (digit > 9){
                digit -= 9;
            }
        }
        sum += digit;
        double_next = !double_next;
    }
    return (sum % 10)==0;
}

int main(void){
    char n[20];
    bool is_valid = false;

    do{
        printf("Enter your card number: ");
        if (scanf("%[^\n]",n) != 1){
            printf("Error: Invalid number\n");
            int c;
            while((c = getchar()) != '\n' && c != EOF);
            continue;
        }

        is_valid = is_numeric(n);

        if (is_valid){
            if(luhn(n)){
                printf("Real.");
            }else{
                printf("Fake.");
            }
        }
        else{
            printf("Invalid number.Please enter only numeric characters.\n");
        }
    }while(!is_valid);
    
    return 0;
}