---
title: 스택
---

> In computer science, a stack is an abstract data type that serves as a collection of elements, with two main principal operations:

>- Push, which adds an element to the collection, and
>- Pop, which removes the most recently added element that was not yet removed.
>
> -wikipedia

**LIFO (last in, first out)**

## ADT

``` {class="language-c"}
void StackInit(Stack *pstack);

bool SIsEmpty(Stack *pstack);

void SPush(Stack *pstack, Data data);

Data SPop(Stack *pstack);
// 데이터가 하나 이상 존재함이 보장되어야 한다. 

Data SPeek(Stack *pstack);
// 데이터가 하나 이상 존재함이 보장되어야 한다. 
```
