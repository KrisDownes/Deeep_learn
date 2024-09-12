#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

// Define the structures for the headers
typedef struct {
    short bfType;
    int bfSize;
    short bfReserved1;
    short bfReserved2;
    int bfOffBits;
} __attribute__((packed)) BITMAPFILEHEADER;

typedef struct {
    int biSize;
    int biWidth;
    int biHeight;
    short biPlanes;
    short biBitCount;
    int biCompression;
    int biSizeImage;
    int biXPelsPerMeter;
    int biYPelsPerMeter;
    int biClrUsed;
    int biClrImportant;
} __attribute__((packed)) BITMAPINFOHEADER;

void applyGrayscaleFilter(unsigned char *pixel, int bytesPerPixel){
    if (bytesPerPixel >= 3){
        unsigned char gray = (unsigned char)(0.299 * pixel[2] + 0.587 * pixel[1] + 0.114 * pixel[0]);
        pixel[0] = pixel[1] = pixel[2] = gray;
    }
}

// Reflection filter
void applyReflectionFilter(unsigned char *imageData, int width, int height, int bytesPerPixel, int padding){
    int rowSize = width * bytesPerPixel + padding;
    unsigned char *tempRow = malloc(width * bytesPerPixel);

    if (tempRow == NULL){
        printf("Memory allocation failed for temp row.\n");
        return;
    }

    for (int y = 0; y < height; y++){
        unsigned char *row = imageData + y *rowSize;

        // Copy row to temp buffer
        memcpy(tempRow, row, width * bytesPerPixel);

        // Reverse the row
        for (int x = 0; x < width; x++){
            int leftPixel = x * bytesPerPixel;
            int rightPixel = (width - 1 - x) * bytesPerPixel;

            for (int b = 0; b < bytesPerPixel; b++){
                row[leftPixel + b] = tempRow[rightPixel + b];
            }
        }
    }
    free(tempRow);
}

// Blur Filter
void applyBlurFilter(unsigned char *imageData, int width, int height, int bytesPerPixel, int padding){
    int rowSize = width * bytesPerPixel + padding;
    unsigned char *tempData = malloc(height * rowSize);
    if (tempData == NULL){
        printf("Memory allocation for blur failed.\n");
        return;
    }
    memcpy(tempData,imageData,height * rowSize);

    for (int y = 1; y < height - 1; y++){
        for (int x = 1; x < width - 1;x++){
            for (int c = 0; c < 3; c++){
                int sum = 0;
                for (int dy = -1; dy <= 1; dy++){
                    for (int dx = -1; dx <= 1; dx++){
                        int currentPixel = ((y + dy) * rowSize) + ((x + dx) * bytesPerPixel) + c;
                        sum += tempData[currentPixel];
                    }
                }
                int currentPixel = (y * rowSize) + (x * bytesPerPixel) + c;
                imageData[currentPixel] = (unsigned char)(sum / 9);
            }
        }
    }
    free(tempData);
}

// Function to write BMP file
int writeBMPFile(const char *filename, BITMAPFILEHEADER *fileHeader, BITMAPINFOHEADER *infoHeader, unsigned char *imageData){
    FILE *file = fopen(filename, "wb");
    if (file == NULL){
        printf("Could not create file: %s\n",strerror(errno));
        return 0;
    }

    //Write Header
    if (fwrite(fileHeader,sizeof(BITMAPFILEHEADER), 1, file) != 1){
        printf("Error writing file header\n");
        fclose(file);
        return 0;
    }

    //Write infoHeader
    if (fwrite(infoHeader,sizeof(BITMAPINFOHEADER), 1, file) != 1){
        printf("Error writing infoHeader\n");
        fclose(file);
        return 0;
    }

    int bytesPerPixel = infoHeader->biBitCount / 8;
    int padding = (4 - (infoHeader->biWidth * bytesPerPixel) % 4) % 4;
    int rowSize = infoHeader->biWidth * bytesPerPixel + padding;

    for (int i = 0; i < infoHeader->biHeight; i++){
        if (fwrite(imageData + i * rowSize, 1,rowSize, file) != rowSize){
            printf("Error writing image data\n");
            fclose(file);
            return 0;
        }
    }
    fclose(file);
    return 1;
}

int main(int argc, char *argv[]) {

    if (argc != 4){
        printf("Please enter <filter-flag> <input-file> <output-file>.\n");
        return 1;
    }

    const char *filterFlag = argv[1];
    const char *inputFile = argv[2];
    const char *outputFile = argv[3];


    FILE *input = fopen(inputFile, "rb");
    if (input == NULL) {
        printf("Could not open file: %s\n", strerror(errno));
        return 1;
    }

    BITMAPFILEHEADER fileHeader;
    BITMAPINFOHEADER infoHeader;

    // Read the file header
    if (fread(&fileHeader, sizeof(BITMAPFILEHEADER), 1, input) != 1) {
        printf("Error reading file header\n");
        fclose(input);
        return 1;
    }

    // Check if it's a BMP file
    if (fileHeader.bfType != 0x4D42) { // "BM" in little endian
        printf("Not a BMP file\n");
        fclose(input);
        return 1;
    }

    // Read the info header
    if (fread(&infoHeader, sizeof(BITMAPINFOHEADER), 1, input) != 1) {
        printf("Error reading info header\n");
        fclose(input);
        return 1;
    }

    // Print the header information
    printf("File Type: BM\n");
    printf("File Size: %d bytes\n", fileHeader.bfSize);
    printf("Offset to Pixel Data: %d bytes\n", fileHeader.bfOffBits);
    printf("Width: %d pixels\n", infoHeader.biWidth);
    printf("Height: %d pixels\n", infoHeader.biHeight);
    printf("Bits Per Pixel: %d\n", infoHeader.biBitCount);
    printf("Compression: %d\n", infoHeader.biCompression);


    // Calculate image size and allocate memory
    int bytesPerPixel = infoHeader.biBitCount / 8;
    int padding = (4 - (infoHeader.biWidth * bytesPerPixel) % 4) % 4;
    int rowSize = infoHeader.biWidth * bytesPerPixel + padding;
    int imageSize = rowSize * infoHeader.biHeight;

    unsigned char *imageData = malloc(imageSize);
    if (imageData == NULL){
        printf("Memory allocation failed.\n");
        fclose(input);
        return 1;
    }


    // Allocate memory for one row of pixels
    unsigned char *row = malloc(infoHeader.biWidth * bytesPerPixel);
    if (row == NULL) {
        printf("Memory allocation failed\n");
        fclose(input);
        return 1;
    }
    // Seek to the pixel data
    if (fseek(input, fileHeader.bfOffBits, SEEK_SET) != 0) {
        printf("Error seeking to pixel data\n");
        free(imageData);
        fclose(input);
        return 1;
    }

    // Read the image data
    if (fread(imageData,1,imageSize,input) != imageSize){
        printf("Error reading image data\n");
        free(imageData);
        fclose(input);
        return 1;
    }

    fclose(input);

    // Apply the requested filter

    if (strcmp(filterFlag,"-g") == 0){
        for (int i = 0; i < infoHeader.biHeight;i++){
            for (int j =0; j < infoHeader.biWidth; j++){
                int pixelOffset = i * rowSize + j * bytesPerPixel;
                applyGrayscaleFilter(&imageData[pixelOffset],bytesPerPixel);
                printf("Grayscale filter applied\n");
            }
        }
    } else if (strcmp(filterFlag, "-b") == 0){
        applyBlurFilter(imageData,infoHeader.biWidth,infoHeader.biHeight,bytesPerPixel,padding);
        printf("Blur filter applied\n");
    }else if (strcmp(filterFlag,"-r") == 0){
        applyReflectionFilter(imageData,infoHeader.biWidth,infoHeader.biHeight,bytesPerPixel,padding);
        printf("Reflection filter applied.\n");
    } else {
        printf("Unknown filter flag %s\n",filterFlag);
        free(imageData);
        return 1;
    }
    // Write modified image to new file
    if (!writeBMPFile(outputFile, &fileHeader, &infoHeader, imageData)){
        printf("Error writing output file.\n");
        free(imageData);
        return 1;
    }
    free(imageData);
    return 0;

}