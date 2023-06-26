#include <stdio.h>
#include <string.h>
#include <assert.h>

char** reconstructMatrix(int sizeX, int sizeY, char ** strings){
    
}

void freeCMatrix(char ** cMatrix){
    
}

void test(){
    printf("testing...\n");
}

int testInterface(int sizeX, int sizeY, int *x, int *y, char *string){
    assert(strcmp(string,"123456789")==0);
    printf("sizex: %d, sizey: %d\n");
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

//  compilation prompt: 
//  > c:/mingw64/bin/gcc -m64 -fPIC -shared -o lib/cfunctions.so src/cfunctions.c