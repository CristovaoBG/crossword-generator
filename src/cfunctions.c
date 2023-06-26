#include <stdio.h>
#include <string.h>

char** reconstructMatrix(int sizeX, int sizeY, char ** strings){
    
}

void freeCMatrix(char ** cMatrix){
    
}

void test(){
    printf("testing...\n");
}

int testInterface(int sizeX, int sizeY, int *x, int *y, char *string){
    *x = 2;
    *y = 3;
    printf("sizeX: %d, sizeY: %d\nstring: %s\n",sizeX,sizeY,string);
    int i = 0;
    while( string[i]!='\0'){
        string[i] = i + 'a';
        i++;
    }
    return 1;
}

//  compilation prompt: 
//  > c:/mingw64/bin/gcc -m64 -fPIC -shared -o lib/cfunctions.so src/cfunctions.c