//install with:
//linux/win:    sudo apt update
//              sudo apt install build-essential gdb
//osx:          brew install gcc gdb
//compile with: gcc -o helloc helloc.cpp
#include <stdio.h>

int main(int argc,char **argv){
    printf("Hello World! %d\n",fib(3));
    return 0;
}
