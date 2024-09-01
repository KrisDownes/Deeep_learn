#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_LENGTH 1000

int word_count(const char *paragraph){
    int count = 0;
    int in_word = 0;

    for (int i = 0; paragraph[i] != '\0'; i++){
        if (isspace(paragraph[i])){
            in_word = 0;
        } else if (!in_word){
            count++;
            in_word = 1;
        }
    }
    return count;
}

int letter_count(const char *paragraph){
    int letter_count = 0;
    int in_word = 0;

    for (int i = 0; paragraph[i] != '\0'; i++){
        if (isalpha(paragraph[i])){
            letter_count++;
        }
    }
    return letter_count;
}

int sentence_count(const char *paragraph){
    int count = 0;

    for (int i = 0; paragraph[i] != '\0'; i++){
        if (paragraph[i] == '.' || paragraph[i] == '!' || paragraph[i] == '?'){
            count++;
        }
    }
    return count;
}



int main(void){
    char paragraph[MAX_LENGTH];
    

    printf("Text: ");
    fgets(paragraph,MAX_LENGTH,stdin);

    float avg_letters_per_word = (float)letter_count(paragraph) / word_count(paragraph);
    float avg_letters_per_100_words = avg_letters_per_word * 100;

    float avg_sentences_per_word = (float)sentence_count(paragraph) / word_count(paragraph);
    float avg_sentences_per_100 = avg_sentences_per_word*100;

    float index = (0.0588 * avg_letters_per_100_words) - (avg_sentences_per_100 * 0.296) - 15.8; 
    
    printf("Average letters per word: %.2f\n", avg_letters_per_word);
    printf("Average letters per 100 words: %.2f\n", avg_letters_per_100_words);
    printf("Average sentences per word: %.2f\n",avg_sentences_per_word);
    printf("Average sentences per 100 words: %.2f\n",avg_sentences_per_100);
    printf("Readability index: %.2f\n",index);
    return 0;
}