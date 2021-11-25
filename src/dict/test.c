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

typedef struct _node
{
    LData data;
    struct _node *next;
} Node;

typedef struct _linkedList
{
    Node *head;
    Node *cur;
    Node *prev;
    int size;
    bool (*AreInIncreasingOrder)(LData *a, LData *b);
} LinkedList;

typedef LinkedList List;

void ListInit(List *plist)
{
    plist->head = NULL;
    plist->size = 0;
    plist->AreInIncreasingOrder = NULL;
}

void LInsert(List *plist, LData data)
{
    Node *node = malloc(sizeof(Node));
    node->data = data;
    (plist->size)++;
    if (!plist->head)
    {
        node->next = NULL;
        plist->head = node;
        return;
    }
    if (plist->AreInIncreasingOrder)
    {
        if (plist->AreInIncreasingOrder(&data, &(plist->head->data)))
        {
            node->next = plist->head;
            plist->head = node;
            return;
        }
        Node *cur = plist->head;
        while (cur->next && plist->AreInIncreasingOrder(&cur->next->data, &data))
            cur = cur->next;
        node->next = cur->next;
        cur->next = node;
    }
    else
    {
        node->next = plist->head->next;
        plist->head = node;
    }
}

bool LFirst(List *plist, LData *data)
{
    if (!LCount(plist))
        return false;
    plist->prev = NULL;
    plist->cur = plist->head;
    if (data)
        *data = plist->cur->data;
    return true;
}

bool LNext(List *plist, LData *data)
{
    if (!(plist->cur->next))
        return false;
    plist->prev = plist->cur;
    plist->cur = plist->cur->next;
    if (data)
        *data = plist->cur->data;
    return true;
}

int LCount(List *plist) { return plist->size; }

void LRemove(List *plist)
{
    (plist->size)--;
    if (!plist->prev)
    {
        plist->head = plist->head->next;
        free(plist->cur);
        plist->cur = plist->head;
        return;
    }
    plist->prev->next = plist->cur->next;
    free(plist->cur);
    plist->cur = plist->prev;
}

void LClear(List *plist)
{
    while (LFirst(plist, NULL))
    {
        LRemove(plist);
    }
}

void SetSortRule(List *plist, bool (*AreInIncreasingOrder)(LData *a, LData *b))
{
    plist->AreInIncreasingOrder = AreInIncreasingOrder;
}

int main(void)
{
    int testDataSize = 7;
    int xList[] = {3, 1, 4, 1, 5, 9, 2};
    int yList[] = {6, 8, 3, 5, 8, 9, 7};
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
    SetSortRule(&list, IsPointIncreasingOrder);

    for (int i = 0; i < testDataSize; i++)
        LInsert(&list, testData[i]);

    printf("Data Count: %d\n", LCount(&list));

    if (LFirst(&list, &data))
    {
        PrintPoint(&data);
        while (LNext(&list, &data))
            PrintPoint(&data);
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
        PrintPoint(&data);
        while (LNext(&list, &data))
            PrintPoint(&data);
    }
    puts("");
    printf("Data Count: %d\n", LCount(&list));
    LClear(&list);
}

// 열혈책에서 LFirst가 순회 전에 항상 초기화됨을 명시함. 구현을 할 때 이게 영향을 꽤 줌! LInit에서는 before를 신경 쓸 이유가 없다.
// tail 존재 유무, dummy 존재 유무.
// tail에 더미가 있으면 추가할 수가 있나,,,?
// next 함수에서 data 참조와 next 이동의 순서 관계도 포인트
// cur이 6에 있다는 것은 6이 참조되었다는 뜻.
// 책 예제처럼 굳이 malloc을 써서 반환해야할까?
// cur->next->data 에는 무조건 데이터가 있음
// c언어에서 NULL은 포인터에 적용됨.
// https://stackoverflow.com/questions/4141666/why-sizeof-is-equivalent-to-1-and-sizeofnull-is-equivalent-to-4-in-c-langu/4141699
// while문을 해석하는 감 익히기.
// 책에는 free하는 부분이 없어서 내가 추가했다.
// 전달된 포인터가 NULL일 가능성은 생각하지 않아도 되나??
// AreInIncreasingOrder로 이름을 바꿨다.
// LRemove가 값을 반환할 필요가 있을까? popLast 같은거면 몰라도,,,
// 더미 노드 더하는 테크닉 멋져,,,! 이거 없으면 숨쉴 때마다 head 예외 생각해야 함. sorted insert 구현할 때 정신나감. cur 뒤에 들어가는게 전제인데 이러면 맨 앞에 넣을 수가 없음.
// LRemove는 개수가 0이 아님이 보장되어있다고 보자.