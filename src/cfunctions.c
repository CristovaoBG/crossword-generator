#include <stdio.h>
#include <string.h>
#include <assert.h>

#define true 1
#define false 0
#define MAX_ROWS 100
#define MAX_COLS 100
#define MAX_LINE 100
#define VOID_CHAR ' '
#define WORD_WRAPPER_CHAR '.'

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
            matrix[i][j] = VOID_CHAR;
        }
    }

    while (token != NULL) {

        sscanf(token, "%d %d %c %s", &x, &y, &direction, word);
        int len = strlen(word);
        int dx = (direction == '-');
        int dy = (direction == '|');
        
        // adiciona '.' no  inicio, se houver espaco
        if ((dx && x>0) || (dy && y>0)) matrix[y -1 * dy][x -1 * dx] = WORD_WRAPPER_CHAR;

        for (int j = 0; j < len; j++) {
            matrix[y + j * dy][x + j * dx] = word[j];
        }
            
        matrix[y + len * dy][x + len * dx] = WORD_WRAPPER_CHAR;
        
        token = strtok(NULL, "\n"); // passa para a próxima linha
        
        }
    return NULL;
}

void get_line_string( int width, int height, char matrix[MAX_COLS][MAX_ROWS], char line_string[MAX_LINE], int line_num, char direction){
    int i,j,step;
    int count_end = width > height? width : height; //otimizavel?
    // TODO: ver se essa implementacao eh mais rapida
    // int dx = (direction == '-');
    // int dy = (direction == '|');

    // for (step = 0; step < coun_end? width:height; step++){
    //     matrix[y + j * dy][x + j * dx] = word[j];
    // }


    if(direction == 'h'){
        strncpy(line_string,matrix[line_num],width);
        line_string[width+1] = '\0';
        return;
    }
    //else
    for(step = 0; step < height; step ++){
        line_string[step] = matrix[step][line_num];
    }
    line_string[step] = '\0';


}

void c_best_place_in_line(int height, int width, char direction, char* word, char* matrix_string, int line, int* score_output, int* offset_output){
    int i, j;
    char matrix[MAX_ROWS][MAX_COLS];
    char line_string[MAX_LINE], word_wrapped[MAX_LINE];
    string_to_matrix(matrix_string, matrix, width, height);

    for (i = 0; i < 14; i++) {
        for (int j = 0; j < 14; j++) {
            printf("%c ", matrix[i][j]);
        }
        printf("\n");
    }

    get_line_string(width, height, matrix, line_string, line, direction);
    // coloca word wrapper
    strcpy(&word_wrapped[1],word);

    

    word_wrapped[0] = WORD_WRAPPER_CHAR;
    word_wrapped[strlen(word_wrapped)] = WORD_WRAPPER_CHAR;
    word_wrapped[strlen(word_wrapped)+1] = '\0';
    
    //get_line_string(width, height, matrix, line_string, 0, 'h');
    static int len_word_wrapped = strlen(word_wrapped);
    static int len_line_str = strlen(line_string);
    int offset, score, best_score = -1;
    int fits;
    int best_offset = -1;
    // verifica no inicio
    fits = true;
    score = 0;
    for(i=0; i<len_word_wrapped-1; i++){      
        printf("ww: %c ls: %c\n",word_wrapped[i+1],line_string[i]);
        if (word_wrapped[i+1] != line_string[i]
            &&
            line_string[i] != VOID_CHAR)
        {
            fits = false;
            break;
        }
        // else
        if (line_string[i] != VOID_CHAR && line_string[i] != WORD_WRAPPER_CHAR){
            score++; // intersection counter
        }
    }
    if(fits && score>best_score){
        best_score = score;
        best_offset = offset;
        printf("\nFITS! score: %d offset:%d\n",score,offset);
    }   
    
    //verifica no meio
    for(offset=1; offset<len_line_str-len_word_wrapped-1; offset++){
        //printf("------%d------",line_string);
        printf("---1---");
        fits = true;
        score = 0;
        for(i=0; i<len_word_wrapped; i++){      
            printf("ww: %c ls: %c\n",word_wrapped[i],line_string[offset + i]);
            if (word_wrapped[i] != line_string[offset + i]
                &&
                line_string[offset + i] != VOID_CHAR)
            {
                fits = false;
                break;
            }
            // else
            if (line_string[offset + i] != VOID_CHAR && line_string[offset + i] != WORD_WRAPPER_CHAR){
                score++; // intersection counter
                printf("---3---");
            }
        }
        if(fits && score>best_score){
            best_score = score;
            best_offset = offset;
            printf("\nFITS! score: %d offset:%d\n",score,offset);
        }
    }
    // verifica no final
    fits = true;
    score = 0;
    for(i = len_line_str-len_word_wrapped+1; i<len_line_str; i++){      
        printf("ww: %c ls: %c\n",word_wrapped[i+1],line_string[i]);
        if (word_wrapped[i] != line_string[i]
            &&
            line_string[i] != VOID_CHAR)
        {
            fits = false;
            break;
        }
        // else
        if (line_string[i] != VOID_CHAR && line_string[i] != WORD_WRAPPER_CHAR){
            score++; // intersection counter
        }
    }
    if(fits && score>best_score){
        best_score = score;
        best_offset = offset;
        printf("\nFITS! score: %d offset:%d\n",score,offset);
    }  


    *offset_output = best_offset;
    *score_output = best_score;
}

//  compilation prompt: 
//  > c:/mingw64/bin/gcc -m64 -fPIC -shared -o lib/cfunctions.so src/cfunctions.c