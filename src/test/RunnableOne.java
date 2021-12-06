package test;

public class RunnableOne implements Runnable {

    // int count = 0;
    static int count = 0;

    public void run() {
        for (int i = 0; i < 10000; i++)
            count++;
    }
}
