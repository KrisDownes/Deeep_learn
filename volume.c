#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <stdint.h>

const int HEADER_SIZE = 44;

int main(int argc, char *argv[]){
    if (argc != 4){
        printf("Usage: %s <input_filename> <output_filename> <factor>\n",argv[0]);
        return 1;
    }

    FILE *input = fopen(argv[1], "rb");
    if (input == NULL){
        printf("Could not open file.\n");
        fclose(input);
        return 1;
    }

    FILE *output = fopen(argv[2], "wb");
    if (output == NULL){
        printf("Could not open output file.\n");
        fclose(output);
        return 1;
    }

    float factor = atof(argv[3]);

    uint8_t header[HEADER_SIZE];
    fread(header,HEADER_SIZE,1,input);
    fwrite(header,HEADER_SIZE,1,output);

    uint16_t buffer;

    while (fread(&buffer,sizeof(uint16_t),1,input) == 1){
        buffer = (uint16_t)(buffer * factor);
        fwrite(&buffer,sizeof(uint16_t),1,output);

    }
    fclose(input);
    fclose(output);
    return 0;

}
