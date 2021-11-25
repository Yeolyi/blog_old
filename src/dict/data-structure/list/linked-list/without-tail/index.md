---
title: 꼬리 없는 연결 리스트 구현
---

## 더미 노드가 없는 끔찍한 구현

``` {class="language-c"}
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
```

## 더미 노드가 있는 구현

``` {class="language-c"}
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
    int len;
    bool (*areInIncreasingOrder)(LData *a, LData *b);
} LinkedList;

typedef LinkedList List;

void ListInit(List *plist)
{
    Node *dummy = malloc(sizeof(Node));
    plist->head = dummy;
    plist->cur = dummy;
    plist->len = 0;
    plist->areInIncreasingOrder = NULL;
}

void LInsertSorted(List *plist, LData data)
{
    Node *node = malloc(sizeof(Node));
    node->data = data;
    Node *cur = plist->head;
    while (cur->next != NULL && plist->areInIncreasingOrder(&cur->next->data, &data))
        cur = cur->next;
    node->next = cur->next;
    cur->next = node;
    (plist->len)++;
}

void LInsert(List *plist, LData data)
{
    Node *node = malloc(sizeof(Node));
    node->data = data;
    if (plist->areInIncreasingOrder)
    {
        LInsertSorted(plist, data);
    }
    else
    {
        node->next = plist->head->next;
        plist->head->next = node;
        (plist->len)++;
    }
}

bool LFirst(List *plist, LData *data)
{
    if ((plist->len) == 0)
    {
        return false;
    }
    plist->prev = plist->head;
    plist->cur = plist->head->next;
    *data = plist->cur->data;
    return true;
}

bool LNext(List *plist, LData *data)
{
    if (plist->cur->next == NULL)
    {
        return false;
    }
    plist->prev = plist->cur;
    plist->cur = plist->cur->next;
    *data = plist->cur->data;
    return true;
}

int LCount(List *plist)
{
    return plist->len;
}

LData LRemove(List *plist)
{
    plist->prev->next = plist->cur->next;
    LData ret = plist->cur->data;
    free(plist->cur);
    plist->cur = plist->prev;
    return ret;
}

void SetSortRule(List *plist, bool (*areInIncreasingOrder)(LData *a, LData *b))
{
    plist->areInIncreasingOrder = areInIncreasingOrder;
}

```