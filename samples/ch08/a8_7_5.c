#include <stdio.h>

int main() {
    int data[] = {1,2,3,4};
    int* curarr = &data[1];
    printf("%d\n", curarr[-1]);
    return 0;
}
