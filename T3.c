#include <stdio.h>
#include <stdlib.h>

/*
int * m1(void)
{
    int v1 = 11;
    printf("&v1 = %p\n", &v1);
    int *p1;
    p1 = (int *)malloc(5*sizeof(int));
    printf("p1 = %p\n", p1);

    int i;
    for (i = 0; i < 5; i++)
    {
        *(p1+i) = 100+i;
        //p1[i] = 100+i;
    }

    printf("p1_1 = %d\n", *(p1+1));
    printf("p1_2 = %p\n", p1);

    free(p1);
    p1 = NULL;
    p1 = &v1;
    //p1 = NULL;
    printf("p1_3 = %p\n", p1);


    //int a1[5] = {1, 2, 3, 4, 5};
    return p1;
}

int main(void)
{
    int *p1 = m1();
    printf("p1 = %p\n", p1);
    return 0;
}
*/
