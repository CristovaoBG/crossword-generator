#include <stdio.h>

char** reconstructMatrix(int sizeX, int sizeY, char ** strings){
    
}

void freeCMatrix(char ** cMatrix){
    
}

void test(){
    printf("testing...\n");
}

void testInterface(int sizeX, int sizeY, int *x, int *y, char *crossWordString){
    *x = 2;
    *y = 3;
    for(int i=0; i < sizeX; i++){
        for(int j=0; j < sizeY; j++){
            printf(&crossWordString[i*sizeX+j]);
            crossWordString[i*sizeX+j] = 'a' + i+3*j;
        }
    }
}

//  compilation prompt: 
//  > c:/mingw64/bin/gcc -m64 -fPIC -shared -o lib/cfunctions.so src/cfunctions.c