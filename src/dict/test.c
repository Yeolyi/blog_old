#include <stdio.h>
#include <stdbool.h>

#define LIST_LEN 100
typedef int LData;

typedef struct __ArrayList
{
    LData arr[LIST_LEN];
    int numOfData;
    int curPos;
} ArrayList;

typedef ArrayList List;

void ListInit(List *plist)
{
    plist->numOfData = 0;
    plist->curPos = -1;
}

void LInsert(List *plist, LData data)
{
    if (plist->numOfData >= LIST_LEN)
    {
        puts("저장할 공간이 없습니다");
        return;
    }
    plist->arr[plist->numOfData] = data;
    plist->numOfData++;
}

bool LFirst(List *plist, LData *pdata)
{
    if (plist->numOfData == 0)
        return false;
    plist->curPos = 0;
    *pdata = plist->arr[plist->curPos];
    return true;
}

bool LNext(List *plist, LData *pdata)
{
    if (plist->curPos >= (plist->numOfData) - 1)
        return false;
    (plist->curPos)++;
    *pdata = plist->arr[plist->curPos];
    return true;
}

int LCount(List *plist)
{
    return plist->numOfData;
}

LData LRemove(List *plist)
{
    int ret = plist->arr[plist->curPos];
    for (int i = plist->curPos; i < (plist->numOfData) - 1; i++)
    {
        plist->arr[i] = plist->arr[i + 1];
    }
    (plist->numOfData)--;
    (plist->curPos)--;
    return ret;
}

int main()
{
    printf("%d", 1.5);
}
