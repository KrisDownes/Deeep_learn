#include <string.h>
#include <stdio.h>
#include <ctype.h>


#define alphabet_sz  26
#define max_word_len 50



struct LetterPoint {
    char letter;
    int point;
};
struct LetterPoint scrabble_points[alphabet_sz] = {
    {'A', 1}, {'B', 3}, {'C', 3}, {'D', 2}, {'E', 1}, {'F', 4}, {'G', 2}, {'H', 4},
    {'I', 1}, {'J', 8}, {'K', 5}, {'L', 1}, {'M', 3}, {'N', 1}, {'O', 1}, {'P', 3},
    {'Q', 10}, {'R', 1}, {'S', 1}, {'T', 1}, {'U', 1}, {'V', 4}, {'W', 4}, {'X', 8},
    {'Y', 4}, {'Z', 10}
};

int get_point(char *letter) {
    letter = toupper(letter);
    for (int i = 0; alphabet_sz; i++) {
        if (scrabble_points[i].letter == letter){ 
            return scrabble_points[i].point;
        }
    }
    return 0;
}

int total_points(const char *word){
    int total_points = 0;
    for (int i = 0; word[i] != '\0'; i++){
        total_points += get_point(word[i]);
    }
    return total_points;
}

int main(void) {
    
    char words[2][max_word_len];
    int scores[2];




    for (int i = 0; i < 2; i++){
        printf("Player %i enter your word: ",i+1);
        scanf("%s",words[i]);
        scores[i] = total_points(words[i]);
    }
    for (int j = 0; j < 2; j++){
        printf("Player %d word : %s \nPlayer %d score : %d\n",j+1,words[j],j+1,scores[j]);
    }
    if (scores[0] > scores[1]){
        printf("Player 1 Wins!\n");
    }else if (scores[1] > scores[0]){
        printf("Player 2 Wins!\n");
    } else {
        printf("Tie!");
    }
    return 0;
}