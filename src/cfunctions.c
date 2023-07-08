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
#define VERT_DIR '|'
#define HORI_DIR '-'
#define BOTH_DIR '+'

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

char** string_to_matrix(char *matrixString, char matrix[MAX_COLS][MAX_ROWS], char direction_matrix[MAX_COLS][MAX_ROWS], int width,int height){
    char* token = strtok(matrixString, "\n");
    int x, y, i, j;
    char direction;
    char word[100];
    // clear matrix first
    for (i=0; i< width; i++){
        for (j=0; j<height; j++){
            matrix[i][j] = VOID_CHAR;
            direction_matrix[i][j] = VOID_CHAR;
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
            char current_direction = direction_matrix[y + j * dy][x + j * dx];
            if(current_direction != VOID_CHAR){
              direction_matrix[y + j * dy][x + j * dx] = BOTH_DIR;
            }
            else{
              direction_matrix[y + j * dy][x + j * dx] = direction;
            }
        }

        matrix[y + len * dy][x + len * dx] = WORD_WRAPPER_CHAR;

        token = strtok(NULL, "\n"); // passa para a próxima linha

        }
    return NULL;
}

void get_line_string( int width, int height, char matrix[MAX_COLS][MAX_ROWS],char direction_matrix[MAX_COLS][MAX_ROWS], char line_string[MAX_LINE],char direction_string[MAX_LINE], int line_num, char direction){
    int step = 0;

    if(direction == 'h'){
        #ifdef DEBUG
        printf("DECODING LINE WITH STRNCPY\n");
        #endif
        strncpy(line_string,matrix[line_num],width);
        strncpy(direction_string,direction_matrix[line_num],width);
        line_string[width+1] = '\0';
        direction_string[width+1] = '\0';
        return;
    }
    //else
    #ifdef DEBUG
    printf("DECODING LINE WITH FOR LOOP\n");
    #endif
    for(step = 0; step < height; step ++){
        line_string[step] = matrix[step][line_num];
        direction_string[step] = direction_matrix[step][line_num];
    }
    line_string[step] = '\0';
    direction_string[step] = '\0';
}

void c_best_place_in_line(int height, int width, char direction, char* word, char* matrix_string, int line, int* offset_output, int* score_output){
    int i, j;
    char matrix[MAX_ROWS][MAX_COLS], direction_matrix[MAX_ROWS][MAX_COLS];
    char line_string[MAX_LINE], word_wrapped[MAX_LINE], direction_string[MAX_LINE];
    string_to_matrix(matrix_string, matrix, direction_matrix, width, height);

    #ifdef DEBUG
    printf("RECONSTRUCTED MATRIX IN C CODE:\n");
    for (i = 0; i < 14; i++) {
         for (int j = 0; j < 14; j++) {
             printf("%c ", matrix[j][i]);
         }
         printf("\n\n");
    }

    for (i = 0; i < 14; i++) {
         for (int j = 0; j < 14; j++) {
             printf("%c ", direction_matrix[j][i]);
         }
         printf("\n");
    }

    printf("GETTING LINE STRING...\n");
    #endif

    get_line_string(width, height, matrix, direction_matrix, line_string, direction_string, line, direction);

    #ifdef DEBUG
    printf("DONE! LINE STRING:\"%s\". SETTING WRAPPER...\n",line_string);
    #endif

    // coloca word wrapper
    const int len_word_naked = strlen(word);
    const int len_word_wrapped = len_word_naked + 2;
    strcpy(&word_wrapped[1],word);
    word_wrapped[0] = WORD_WRAPPER_CHAR;
    word_wrapped[len_word_naked+1] = WORD_WRAPPER_CHAR;
    word_wrapped[len_word_naked+2] = '\0';

    #ifdef DEBUG
    printf("DONE! WORD WRAPPER:\"%s\"\n",word_wrapped);
    #endif

    const int len_line_str = strlen(line_string);
    int offset, score, best_score = -1;
    int fits;
    int best_offset = -1;

    if(len_line_str < len_word_naked){
      *offset_output = -1; //? TODO corrigir isso
      *score_output = -1;
      return;
    }

    // verifica no inicio
    fits = true;
    score = 0;
    for(i=0; i<len_word_wrapped-1 && i<len_line_str; i++){
        if ((word_wrapped[i+1] != line_string[i] && line_string[i] != VOID_CHAR)
            ||
            direction_string[i] == direction
            ||
            direction_string[i] == BOTH_DIR)
        {
            fits = false;

            #ifdef DEBUG
            printf("DONT FIT AT BEGGINING: i:%d word_wrapped[i+1]: \"%c\" line_string[i] = \"%c\"\n",i,word_wrapped[i+1],line_string[i]);
            #endif

            break;
        }
        // else
        if (line_string[i] != VOID_CHAR && line_string[i] != WORD_WRAPPER_CHAR){
            score++; // intersection counter
        }
    }
    if(fits && score>best_score){
        #ifdef DEBUG
        printf("FITS IN THE BEGGINING! score: %d, offset = -1 (sempre -1 no comeco)\n",score);
        #endif
        best_score = score;
        best_offset = 0;
    }

    //verifica no meio
    #ifdef DEBUG
    printf("MIDDLE FOR LOOP SCOPE: len_line_str = %d, len_word_wrapped = %d\n",len_line_str,len_word_wrapped);
    #endif
    for(offset=0; offset <= len_line_str - len_word_wrapped; offset++){ //nao sei ao certo porque <= ao inves de <
        //printf("------%d------",line_string);
        //printf("---1---");
        fits = true;
        score = 0;
        for(i=0; i<len_word_wrapped; i++){
            if ((word_wrapped[i] != line_string[offset + i] && line_string[offset + i] != VOID_CHAR)
                ||
                direction_string[offset + i] == direction
                ||
                direction_string[offset + i] == BOTH_DIR)
            {
                fits = false;
                break;
            }
            // else
            if (line_string[offset + i] != VOID_CHAR && line_string[offset + i] != WORD_WRAPPER_CHAR){
                score++;
            }
        }
        if(fits && score>best_score){
            best_score = score;
            best_offset = offset + 1; //mais um para a origem ser na letra, e nao no wrapper
            #ifdef DEBUG
            printf("FITS IN THE MIDDLE! score: %d, offset = %d\n",score,best_offset);
            #endif
        }
    }
    // verifica no final
    fits = true;
    score = 0;

    for(i = len_line_str-len_word_wrapped+1; i<len_line_str; i++){
        if ((word_wrapped[i-(len_line_str-len_word_wrapped+1)] != line_string[i] && line_string[i] != VOID_CHAR)
            ||
            direction_string[i] == direction
            ||
            direction_string[i] == BOTH_DIR)
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
        best_offset = len_line_str-len_word_wrapped+2; // +2??? #TODO ver porque
        #ifdef DEBUG
        printf("FITS IN THE END! score: %d, offset = %d\n",score,best_offset);
        #endif
    }

    #ifdef DEBUG
    printf("FINISHED! FINAL OFFSET: %d, FINAL SCORE = %d\n",best_offset, best_score);
    #endif

    *offset_output = best_offset - 1; //? TODO corrigir isso
    *score_output = best_score;
}

//  compilation prompt:
//  > c:/mingw64/bin/gcc -m64 -fPIC -shared -o lib/cfunctions.so src/cfunctions.c
//  for debug:
//  > c:/mingw64/bin/gcc -DDEBUG -m64 -fPIC -shared -o lib/cfunctions.so src/cfunctions.c
