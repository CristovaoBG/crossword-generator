#include <stdio.h>
#include <string.h>
#include <assert.h>

#define MAX_ROWS 100
#define MAX_COLS 100

char** reconstructMatrix(int sizeX, int sizeY, char ** strings){
    
}

void freeCMatrix(char ** cMatrix){
    
}

int test_interface(int sizeX, int sizeY, int *x, int *y, char *string){
    assert(strcmp(string,"123456789")==0);
    printf("sizex: %d, sizey: %d\n",sizeX,sizeY);
    assert(sizeX==3 && sizeY==4);
    *x = 2;
    *y = 3;
    int i = 0;

    while( string[i]!='\0'){
        string[i] = i + 'a';
        i++;
    }
    return 1;
}

char** string_to_matrix(char *matrixString, char matrix[MAX_COLS][MAX_ROWS], int width,int height){
    char* token = strtok(matrixString, "\n"); 
    int x, y, i, j;
    char direction;
    char word[100];
    // clear matrix first
    for (i=0; i< width; i++){
        for (j=0; j<height; j++){
            matrix[i][j] = ' ';
        }
    }

    while (token != NULL) {

        sscanf(token, "%d %d %c %s", &x, &y, &direction, word);
        int len = strlen(word);
        int dx = (direction == '-');
        int dy = (direction == '|');
        
        // adiciona '.' no  inicio, se houver espaco
        if ((dx && x>0) || (dy && y>0)) matrix[y -1 * dy][x -1 * dx] = '.';

        for (int j = 0; j < len; j++) {
            matrix[y + j * dy][x + j * dx] = word[j];
            }
            
        matrix[y + len * dy][x + len * dx] = '.';
        
        token = strtok(NULL, "\n"); // passa para a próxima linha
        
        }
    return NULL;
}

void c_best_place_in_line(int height, int width, char direction, char* word, char* matrixSting, int line, int* x, int* y){
    char matrix[MAX_ROWS][MAX_COLS];
    string_to_matrix(matrixSting, matrix, width, height);

    for (int i = 0; i < 14; i++) {
        for (int j = 0; j < 14; j++) {
            printf("%c ", matrix[i][j]);
        }
        printf("\n");
    }
}

//  compilation prompt: 
//  > c:/mingw64/bin/gcc -m64 -fPIC -shared -o lib/cfunctions.so src/cfunctions.c