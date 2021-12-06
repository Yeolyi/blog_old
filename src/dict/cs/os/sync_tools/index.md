---
title: 프로세스 동기화
---

## 프로세스 동기화

Concurrent access to shared data -> data inconsistency
실행 순서대로 실행되게 보장해야 data consistency를 유지할 수 있다. 

생산자-소비자 문제에서 각각은 버퍼를 사용한다. 각자 쓰고 읽고 싶을 때 하는 비동기적으로 작동. parallel하게 돈다면 문제가 발생하지 않지만 concurrent하면??? 반대 아닌가,,,?  

count로 버퍼에 있는 원소의 개수를 센다고 하자. 제대로 동작 안함. 

```
#include <stdio.h>
#include <pthread.h>

// 전역변수면 무조건 0이었나~?
int sum;

void *run1(void *param)
{
    for (int i = 0; i < 10000; i++)
        sum++;
    pthread_exit(0);
}

void *run2(void *param)
{
    for (int i = 0; i < 10000; i++)
        sum--;
    pthread_exit(0);
}

int main()
{
    pthread_t tid1, tid2;
    pthread_create(&tid1, NULL, run1, NULL);
    pthread_create(&tid2, NULL, run2, NULL);
    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);
    printf("%d", sum);
}
```

c언어로 보니 ++ -- 문장 하나지만 실제로는 레지스터에 count값 옮기고 계산하고 다시 저장하는 과정으로 이루어져있음. 이 사이에서 context switching이 일어날 수 있음. 

Race Condition: 경쟁 상황. 여러 개의 프로세스(쓰레드)가 공유하는 데이터를 concurrent하게 접근/수정하면 결과가 실행 순서에 따라 달라질 수 있다. 

- Synchronization: 특정 시간에 하나의 프로세스만 다룰 수 있게 하기. 

```
package test;

public class RaceCondition {
    public static void main(String[] args) throws Exception {
        RunnableOne run1 = new RunnableOne();
        RunnableOne run2 = new RunnableOne();
        Thread t1 = new Thread(run1);
        Thread t2 = new Thread(run2);
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println("Result: " + RunnableOne.count);
    }
}

package test;

public class RunnableOne implements Runnable {

    // int count = 0;
    static int count = 0;

    public void run() {
        for (int i = 0; i < 10000; i++)
            count++;
    }
}
```

The Critical Section Problem: 임계 영역 문제. N개의 프로세스가 있을 때 각각은 다른 프로세스와 공유되며 임계 영역이라 불리는 코드 segment가 있다. 한 코드가 임계 영역을 실행할 때 다른 애들이 스스로의 임계 영역을 실행하지 못하도록 하자! 

그러면 코드 영역을 다음과 같이 나눌 수 있다. 

- Entry section: 임계 영역에 진입하는 코드. 허가를 요청.  
- Critical section
- Exit section: 허가를 반납. 
- Remainder section: 남는거. 

![](code_section.png)

이 해결책의 세가지 조건. 현실적으로 다 풀기는 어렵다. 아래 두개는 발생하면 피해보자 느낌??

- Mutual Exclusion: 상호배제, 다른 애들 못들어옴. 얘가 제일 기본적인 조건. 
- Progress: 데드락 피하기. 
- Bounded Waiting: 기아 피하기. 

싱글 코어에서 가장 간단한 해결책은 shared variable에 접근 중일때는 인터럽트가 발생하지 않도록 하는 것. 하지만 멀티프로세서 환경에서는 쓸 수 없는 방법이다. 

멀티- 환경에서는 두가지 일반적인 접근법. 

- 비선점형 커널에서는 일단 진입을 하면 자발적 반환 전까지 CPU에서 나오지 않으니 문제가 발생하지 않는다. 근데 비선점형은 요즘 안씀. 
- 선점형 커널은 다루기 어렵지만 훨씬 responsive하기 때문에 사용한다. 

## 동기화 문제의 해결책

소프트웨어적 해결책. 

Dekker's Algorithm. 두 개의 프로세스로 해결
Eisenberg and McGuire's Alrogithm. n개의 프로세스, n-1 turns의 대기 하한선을 가짐. 
Bakery Algorithm. Ramport. 책에서는 안다룸. 

우리가 본격적으로 다룰 Peterson's Algorithm. 고전적임. 

```
#include <stdio.h>
#include <pthread.h>
#include <stdbool.h>

int sum = 0;

int turn;
int flag[2];

void *producer(void *param)
{
    for (int i = 0; i < 10000; i++)
    {
        // entry section
        flag[0] = true;
        turn = 1;
        while (flag[1] && turn == 1)
            ;

        // critical section
        sum++;

        //exit section
        flag[0] = false;
    }
    pthread_exit(0);
}

void *consumer(void *param)
{
    for (int i = 0; i < 10000; i++)
    {
        // entry section
        flag[1] = true;
        turn = 0;
        while (flag[0] && turn == 0)
            ;

        // critical section
        sum--;

        //exit section
        flag[1] = false;
    }
    pthread_exit(0);
}

int main()
{
    pthread_t tid1, tid2;
    pthread_create(&tid1, NULL, producer, NULL);
    pthread_create(&tid2, NULL, consumer, NULL);
    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);
    printf("sum= %d\n", sum);
}
```

동기화가 대부분 일어나지만, 실패하는 경우가 생김. Peterson's solution은 no guarantee! 기계어 레벨로 생각해봐야한다. while 조건을 확인하는 과정에서 context switching이 일어나면?
그래도 algorithmic desciprtion으로 살펴보기에는 좋다. 개념적으로 완벽하다~. 위에 세가지 조건을 다 만족시킴. 

[출처](https://stackoverflow.com/questions/4849077/unable-to-understand-correctness-of-peterson-algorithm)

1) Mutual exclusion - flag[0] and flag[1] can both be true, but turn can only be 0 or 1. Therefore only one of the two critical sections can be executed. The other will spin wait.

2) Progress - If process 0 is in the critical section, then turn = 0 and flag[0] is true. Once it has completed it's critical section (even if something catastrophic happens), it must set flag[0] to false. If process 1 was spin waiting, it will now free as flag[0] != true.

3) Bound-waiting - If Process 1 is waiting, Process 0 can only enter it's critical section once, before process 1 is given the green light, as explained in #2.

n개로 확장할수는 있지만 굳이~. 이론적으로 세가지를 동시에 만족시키는 것에 의미가 있다. 

Hardware-based Solution. 

Atomicity. atomic operation이란 인터럽트 할 수 없는 operation.  

- test_and_set()
- compare_and_swap()

얘네 쓴 구현은 적어도 상호 배제는 해결된다. 

Atomic variable. Compare_and_swap 명령어를 atomic variable을 위한 도구로 사용 가능. Single variable에 대한 race condition을 뭐?

```
package test;

public class Peterson1 {
    static int count = 0;
    static int turn = 0;
    static boolean[] flag = new boolean[2];

    public static void main(String[] args) throws Exception {
        Thread t1 = new Thread(new Producer());
        Thread t2 = new Thread(new Consumer());
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println(Peterson1.count);
    }

    static class Producer implements Runnable {
        public void run() {
            for (int i = 0; i < 10000; i++) {
                flag[0] = true;
                turn = 1;
                while (flag[1] && turn == 1)
                    ;
                count++;
                flag[0] = false;
            }
        }
    }

    static class Consumer implements Runnable {
        public void run() {
            for (int i = 0; i < 10000; i++) {
                flag[1] = true;
                turn = 0;
                while (flag[0] && turn == 0)
                    ;
                count--;
                flag[1] = false;
            }
        }
    }
}

```

Atomic 사용 버전. 아까 100000번 할 때 안되던게 여기서는 되는데, 데드락 문제가 해결되었기 때문인듯. 데드락이 일어난건 어떻게 알지?

```
package test;

import java.util.concurrent.atomic.AtomicBoolean;

public class Peterson2 {
    static int count = 0;
    static int turn = 0;
    static AtomicBoolean[] flag;
    static {
        flag = new AtomicBoolean[2];
        for (int i = 0; i < flag.length; i++)
            flag[i] = new AtomicBoolean();
    }

    public static void main(String[] args) throws Exception {
        Thread t1 = new Thread(new Producer());
        Thread t2 = new Thread(new Consumer());
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println(Peterson1.count);
    }

    static class Producer implements Runnable {
        public void run() {
            for (int i = 0; i < 100000; i++) {
                flag[0].set(true);
                turn = 1;
                while (flag[1].get() && turn == 1)
                    ;
                count++;
                flag[0].set(false);
            }
        }
    }

    static class Consumer implements Runnable {
        public void run() {
            for (int i = 0; i < 100000; i++) {
                flag[1].set(true);
                turn = 0;
                while (flag[0].get() && turn == 0)
                    ;
                count--;
                flag[1].set(false);
            }
        }
    }

}

```

상호배제 해결책 세가지 뮤텍스, 세마포어, 모니터

## 뮤텍스와 세마포어

Higher-level software tools to solve CSP

- Mutex Locks: 동기화를 위한 가장 간단한 도구. 열쇠로 쓰고 열쇠를 반납해라. 
- Semaphore: 가장 보편적. 뮤텍스와 달리 n개도 가능. 
- Monitor: 위 도구의 문제점 해결. Java에서 notify 사용. 
- Linveness: 데드락도 해결

Mutex Lock

mutex: mutual exclusion. 프로세스는 lock을 얻어 임계 영역에 들어가야 한다. 나올때는 lock을 release해야한다. 
acquire(), release(). available: 열쇠가 있는가. 두 함수 모두 atomically 작동되어야한다. compare_and_swap 사용해서 구현 가능.

하지만 Busy waiting 문제가 생김. 멀티프로세싱 시스템에서 다른 프로세스가 잘 쓸 수 있었던 CPU 사이클을 낭비하게 된다. 

Spinlock. Busy waiting을 하는 Mutex lock. 위의 단점에도 불구하고 장점이 있는데, lock을 기다리는 과정에서 context switching이 없다. switching 시간을 아낄 수 있음. 멀티코어에서는 좋은 점도 있음. 

```
#include <stdio.h>
#include <pthread.h>

int sum = 0; // a shared variable

pthread_mutex_t mutex;

void *counter(void *param)
{
    for (int i = 0; i < 100000; i++)
    {
        // entry section
        pthread_mutex_lock(&mutex);
        // critical section
        sum++;
        // exit section
        pthread_mutex_unlock(&mutex);
        //remainder section
    }
    pthread_exit(0);
}

int main()
{
    pthread_t tid1, tid2;
    pthread_mutex_init(&mutex, NULL);
    pthread_create(&tid1, NULL, counter, NULL);
    pthread_create(&tid2, NULL, counter, NULL);
    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);
    printf("sum = %d\n", sum);
}
```

세마포. n개짜리. 신호기라는 뜻. 세마포 S는 두개의 표준 atomic operation으로만 접근 가능한 정수 변수. wait()와 signal(). 열쇠꾸러미가 있다고 생각하자. 열쇠가 있으면 하나 가져가고 다시 돌려놓고. 

Binary Semaphore: mutex lock과 비슷. 0과 1에서 왔다갔다함. 

Counting Semaphore: 가능한 리소스 수대로 초기화시킴. 리소스를 사용할 때 wait로 카운트 값을 감소시킴. 리소스 release할때는 카운트 들림. 카운트 0이면 기다리기. 

얘도 물론 busy waiting함. Busy waiting 대신에 waiting queue에 감으로써 해결할 수 있음. 

세마포 값이 음수일 때, 그 절댓값은 세마포를 대기하고 있는 프로세스들의 수이다

```
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

int sum = 0;

sem_t sem;

void *counter(void *param)
{
    for (int k = 0; k < 10000; k++)
    {
        // entry section
        sem_wait(&sem);
        // critical section
        sum++;
        // exit section
        sem_post(&sem);
        // remainder section
    }
    pthread_exit(0);
}

int main()
{
    pthread_t tid1, tid2;
    sem_init(&sem, 0, 1);
    pthread_create(&tid1, NULL, counter, NULL);
    pthread_create(&tid2, NULL, counter, NULL);
    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);
    printf("sum = %d", sum);
}
```

[Deprecated?](https://stackoverflow.com/questions/27736618/why-are-sem-init-sem-getvalue-sem-destroy-deprecated-on-mac-os-x-and-w)

[참고](https://medium.com/helderco/semaphores-in-mac-os-x-fd7a7418e13b)

sem_init. 0은 프로세스를 어떻게 공유할 것인가. 리눅스에서는 0밖에 못씀. 1은 s=1.

sem_init을 5로 하고 5개의 쓰레드를 만들면 각자 열쇠가 있으니 진입해서 sum++을 함. Race condition이 그대로 발생. sum[5]인 배열이고 각각 접근한다면 5개를 동시에 진입시켜도 됨. 

## 모니터와 자바 동기화

세마포가 편하긴하지만 timing errors가 발생할 수 있다. 디버깅하기 매우 어려움.

wait -> signal 순서를 지키지 않으면 문제가 생김. 따라서 higher-level language construct인 모니터 타입을 사용. 

Conditional Variables. 동기화 매커니즘을 제공해줌. 

자바에서는 moniter-lock, intrinsic-lock을 제공해줌. 쓰레드 동기화를 위한 concurrency mechanism. 
synchronized keyword: 임계영역에 해당하는 코드 블록을 선언할 떄 사용하는 자바 키워드. 해당 코드 블록에는 모니터락을 획득해야 진입 가능. 모니터락을 가진 객체 인스턴스를 지정할 수 있음.

wait() and notify(): 각각 wait와 signal. 쓰레드가 어떤 객체의 wait 메소드를 호출하면 해당 객체의 모니터락을 획득하기 위해 대기 상태로 진입함. notify를 호출하면 해당 객체 모니터에 대기중인 쓰레드 하나를 깨움. notifyAll()은 대기중인 쓰레드 전부를 깨움. 

```
package test;

public class SyncExample1 {
    static class Counter {
        public static int count = 0;

        synchronized public static void increment() {
            count++;
        }
    }

    static class MyRunnable implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < 10000; i++)
                Counter.increment();
        }
    }

    public static void main(String[] args) throws Exception {
        Thread[] threads = new Thread[5];
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(new MyRunnable());
            threads[i].start();
        }
        for (int i = 0; i < threads.length; i++)
            threads[i].join();
        System.out.println("counter = " + Counter.count);
    }
}
```

모니터에 선언된 모든 메소드들은 모니터 안에 있는 변수의 동기화를 의미한다. 객체가 달라지면 모니터가 따로 있는거라서 지들끼리만 동기화됨. 

Liveness. 지금까지 본 애들은 데드락과 bounded-waiting문제를 해결하지 못함. 그것도 해결하는게 Liveness. 

Deadlock. 두개 이상의 프로세스가 영원히 기다리는 것. Waiting queue에 있는 프로세스가 일으킬 수 있는 이벤트를 기다리는 것. P0은 wait(S), wait(Q) P1은 wait(Q), wait(S)일 떄. 

Priority Inversion. 높은 우선순위가 낮은 것에게 밀리는 것. 낮은 우선순위 프로세스가 높은 것에게 필요한 자원을 쓰고있으면(커널 데이터 rw) 기다릴 수밖에 없음. 
Priority inheritance protocol로 회피. H가 소유하고자하는 R1을 L가 가지고 있으면 H의 우선순위를 상속함. 
