---
title: 리스트
---

## 구현 방법에 따른 리스트의 분류

[순차 리스트](array-list)

- 배열을 기반으로 구현된 리스트

[연결 리스트](linked-list)

- 메모리의 동적 할당을 기반으로 구현된 리스트

## 리스트의 기본 특성

데이터를 나란히 저장하며 중복된 데이터의 저장을 막지 않는다. 

> In computer science, a list or sequence is an abstract data type that represents a finite number of ordered values, where the same value may occur more than once.
> - Wikipedia

원소의 추가 순서가 보존될 필요는 없는 것 같다. 

## 실습

구현하려는 리스트의 기본적인 ADT는 다음과 같다. 리스트의 종류에 따라 추가적인 기능이 있을 수 있다. 

``` {class="language-c"}
void ListInit(List *plist);
// 리스트 생성 후 가장 먼저 호출되어야 하는 함수

void LInsert(List *plist, LData *pdata);

bool LFirst(List *plist, LData *pdata);
// 데이터의 참조를 위한 초기화가 진행된다.
// 성공 여부를 반환한다.

bool LNext(List *plist, LData *pdata);
// 다음 데이터를 참조한다. 
// 순차적 참조를 위한 반복 호출이 가능하다.

LData LRemove(List *plist);
// LFirst 혹은 LNext의 마지막 반환 데이터를 삭제한다. 

int LCount(List *plist);
```

테스트를 위해 다음과 같은 구조체와 함수를 정의했다. 자연수 배열에서 자연수를 찾는 것은 웃기니까 ^^;

``` {class="language-c"}
typedef struct __Point
{
    int x;
    int y;
    int level;
} Point;

void printPoint(Point *a)
{
    printf("(%d, %d, level: %d) ", a->x, a->y, a->level);
}
```

테스트를 위한 코드는 다음과 같다. 

``` {class="language-c"}
int main(void)
{
    int testDataSize = 7;
    int xList[] = {3, 1, 4, 1, 5, 9, 2};
    int yList[] = {6, 5, 3, 5, 8, 9, 7};
    int level[] = {3, 2, 3, 8, 4, 6, 2};

    Point *testData = malloc(sizeof(Point) * testDataSize);

    for (int i = 0; i < testDataSize; i++)
    {
        testData[i].x = xList[i];
        testData[i].y = yList[i];
        testData[i].level = level[i];
    }

    List list;
    Point data;
    ListInit(&list);

    for (int i = 0; i < testDataSize; i++)
    {
        LInsert(&list, testData[i]);
    }

    printf("Data Count: %d\n", LCount(&list));

    if (LFirst(&list, &data))
    {
        printPoint(&data);
        while (LNext(&list, &data))
        {
            printPoint(&data);
        }
    }
    puts("");
    if (LFirst(&list, &data))
    {
        if (data.level == 2)
            LRemove(&list);
        while (LNext(&list, &data))
            if (data.level == 2)
                LRemove(&list);
    }
    if (LFirst(&list, &data))
    {
        printPoint(&data);
        while (LNext(&list, &data))
            printPoint(&data);
    }
}
```