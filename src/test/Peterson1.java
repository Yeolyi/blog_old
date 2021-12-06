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
