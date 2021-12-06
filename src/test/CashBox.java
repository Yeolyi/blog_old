package test;

public class CashBox {
    private int[] buffer;
    private int count, in, out;

    public CashBox(int bufferSize) {
        buffer = new int[bufferSize];
        count = in = out = 0;
    }

    synchronized public void give(int money) throws InterruptedException {
        while (count == buffer.length) {
            try {
                wait();
            } catch (InterruptedException e) {
            }
        }
        buffer[in] = money;
        in = (in + 1) % buffer.length;
        count++;
        System.out.printf("용돈 줄게 %d\n", money);
        notify();
    }

    synchronized public int take() throws InterruptedException {
        while (count == 0) {
            try {
                wait();
            } catch (InterruptedException e) {
            }
        }
        int money = buffer[out];
        out = (out + 1) % buffer.length;
        count--;
        System.out.printf("용돈 받을게 %d\n", money);
        notify();
        return money;
    }
}
