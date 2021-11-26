#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct __Point
{
    int x;
    int y;
    int level;
} Point;

void PrintPoint(Point *a)
{
    printf("(%d, %d, level: %d) ", a->x, a->y, a->level);
}

bool IsPointIncreasingOrder(Point *a, Point *b)
{
    if (a->x == b->x)
        return a->y < b->y;
    return a->x < b->x;
}

typedef Point LData;

void StackInit(Stack *pstack);

bool SIsEmpty(Stack *pstack);

void SPush(Stack *pstack, Data data);

Data SPop(Stack *pstack);
// 데이터가 하나 이상 존재함이 보장되어야 한다.

Data SPeek(Stack *pstack);
// 데이터가 하나 이상 존재함이 보장되어야 한다.