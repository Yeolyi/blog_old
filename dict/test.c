#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct _PersonInfo
{
    int key;
    char *name;
} PersonInfo;

typedef PersonInfo Data;

typedef struct _BTreeNode
{
    Data data;
    struct _BTreeNode *left;
    struct _BTreeNode *right;
} BTreeNode;

BTreeNode *MakeBTreeNode()
{
    BTreeNode *node = malloc(sizeof(BTreeNode));
    node->left = NULL;
    node->right = NULL;
    return node;
}

Data GetData(BTreeNode *bt)
{
    return bt->data;
}

void SetData(BTreeNode *bt, Data data)
{
    bt->data = data;
}

BTreeNode *GetLeftSubTree(BTreeNode *bt)
{
    return bt->left;
}

BTreeNode *GetRightSubTree(BTreeNode *bt)
{
    return bt->right;
}

void PostOrderTraverse(BTreeNode *main, void (*Transform)(BTreeNode *))
{
    if (!(main))
        return;
    PostOrderTraverse(main->left, Transform);
    PostOrderTraverse(main->right, Transform);
    Transform(main);
}

void FreeTreeNode(BTreeNode *main)
{
    free(main);
}

void DeleteTree(BTreeNode *main)
{
    PostOrderTraverse(main, FreeTreeNode);
}

void MakeLeftSubTree(BTreeNode *main, BTreeNode *sub)
{
    main->left = sub;
}

void MakeRightSubTree(BTreeNode *main, BTreeNode *sub)
{
    main->right = sub;
}

void BSTInit(BTreeNode **pRoot)
{
    *pRoot = NULL;
}

void BSTInsert(BTreeNode **pRoot, Data data)
{
    BTreeNode *cur = *pRoot;
    BTreeNode *newNode = MakeBTreeNode();
    newNode->data = data;

    if (!cur)
    {
        *pRoot = MakeBTreeNode();
        (*pRoot)->data = data;
        return;
    }
    while (true)
    {
        if (data.key < cur->data.key)
        {
            if (cur->left)
                cur = cur->left;
            else
            {
                MakeLeftSubTree(cur, newNode);
                return;
            }
        }
        else
        {
            if (cur->right)
                cur = cur->right;
            else
            {
                MakeRightSubTree(cur, newNode);
                return;
            }
        }
    }
}

//NULL때문에 포인터 쓰는 것도 있는건가
BTreeNode *BSTSearch(BTreeNode *cur, int key)
{
    while (true)
    {
        if (!cur)
            return NULL;
        if (cur->data.key == key)
            return cur;
        if (cur->data.key > key)
            cur = cur->left;
        else
            cur = cur->right;
    }
}

void PrintContent(BTreeNode *node)
{
    printf("%s ", node->data.name);
}

void InorderTraverse(BTreeNode *node, void (*Transform)(BTreeNode *))
{
    if (node->left)
        InorderTraverse(node->left, Transform);
    Transform(node);
    if (node->right)
        InorderTraverse(node->right, Transform);
}

int main()
{
    BTreeNode *bstRoot;
    BSTInit(&bstRoot);
    Data dataList[5];
    char *colorNames[5] = {"RED", "ORANGE", "YELLOW", "GREEN", "BLUE"};
    for (int i = 0; i < 5; i++)
    {
        dataList[i].key = i;
        dataList[i].name = colorNames[i];
        BSTInsert(&bstRoot, dataList[i]);
    }
    printf("%s ", BSTSearch(bstRoot, 0)->data.name);
    printf("%s ", BSTSearch(bstRoot, 2)->data.name);
    printf("%s ", BSTSearch(bstRoot, 3)->data.name);
    printf("%s ", BSTSearch(bstRoot, 1)->data.name);
    printf("%s ", BSTSearch(bstRoot, 4)->data.name);
    puts("");
    InorderTraverse(bstRoot, PrintContent);
    return 0;
}