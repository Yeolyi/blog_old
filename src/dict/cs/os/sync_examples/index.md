---
title: 동시성 제어의 고전적 문제들
---

Bounded-Buffer Problem
Producer-Comsumer 문제에서 버퍼를 사용. 생산자는 버퍼를 채우고 소비자는 버퍼를 비운다. 
서로 대칭 구조가 맞아야 한다. 요즘엔 이렇게 어려운건 안씀 ㅋㅎㅋ.


Readers-Writers Problem
여러개의 프로세스들이 concurrent하게 공유 데이터에 접근하지만, 누구는 읽기만 하고 누구는 읽고 쓰고. 
ex. 여러 프로세스들에서 공유되는 데이터베이스. 
그렇다면 두 개 이상의 reader가 동시에 접근한다고 문제가 발생하지는 않음. 
반대로 writer는 동시에 접근하면 난리남. writer + reader 조합도 마찬가지.

우선순위와 된 구분들.  
first readers-writers problem: 어떤 리더들도 writer가 기다린다고 기다리면 안된다??.  
second readers-writers problem: writer가 기다리고 있으면 reader가 시작 못함?
두 경우 모두 starvation 문제가 발생한다. 

first readers-writers problem
두 개의 뮤텍스를 사용한다. 

스케줄러의 선택에 따라 first second가 갈린다. 
이 문제의 솔루션은 이미 일반화가 되어 reader-writer lock으로 제공된다. 

```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdbool.h>

#define BUFFER_SIZE 5

int buffer[BUFFER_SIZE];

pthread_mutex_t mutex;
sem_t *empty, *full;

int in = 0, out = 0;

void insert_item(int item)
{
    sem_wait(empty);
    pthread_mutex_lock(&mutex);

    buffer[in] = item;
    in = (in + 1) % BUFFER_SIZE;
    printf("Producer: inserted %d\n", item);

    pthread_mutex_unlock(&mutex);
    sem_post(full);
}

void remove_item(int *item)
{
    sem_wait(full);
    pthread_mutex_lock(&mutex);

    *item = buffer[out];
    out = (out + 1) % BUFFER_SIZE;
    printf("Consumer: removed %d\n", *item);

    pthread_mutex_unlock(&mutex);
    sem_post(empty);
}

void *producer()
{
    int item;
    while (true)
    {
        usleep((1 + rand() % 5) * 100000);
        item = 1000 + rand() % 1000;
        insert_item(item); // critical section
    }
}

void *consumer()
{
    int item;
    while (true)
    {
        usleep((1 + rand() % 5) * 100000);
        remove_item(&item); // critical section
    }
}

int main()
{
    sem_unlink("empty");
    sem_unlink("full");
    int numOfProducers = 1, numOfConsumers = 1;
    pthread_t pid;

    pthread_mutex_init(&mutex, NULL);
    empty = sem_open("empty", O_CREAT | O_EXCL, 0, 5);
    full = sem_open("full", O_CREAT | O_EXCL, 0, 0);
    //sem_init(empty, 0, 5);
    //sem_init(full, 0, 0);
    srand(time(0));

    for (int i = 0; i < numOfProducers; i++)
        pthread_create(&pid, NULL, producer, NULL);

    for (int i = 0; i < numOfConsumers; i++)
        pthread_create(&pid, NULL, consumer, NULL);

    sleep(3);
    return 0;
}
```
0으로 자꾸 나온건 mac에서 deprecated돼서. sem_wait가 -1이 반환됨. [링크](https://stackoverflow.com/questions/26797126/why-sem-wait-doesnt-wait-semaphore-on-mac-osx)


Dining-Philosophers Problem

상호 배제는 해결했지만 데드락과 기아 문제도 생각해봐야함. 

