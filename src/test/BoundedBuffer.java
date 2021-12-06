package test;

public class BoundedBuffer {

    public static void main(String[] args) {
        CashBox cashBox = new CashBox(5);
        Thread[] producers = new Thread[1];
        Thread[] consumers = new Thread[1];
        for (int i = 0; i < producers.length; i++) {
            producers[i] = new Thread(new ProdRunner(cashBox));
            producers[i].start();
        }
        for (int i = 0; i < consumers.length; i++) {
            consumers[i] = new Thread(new ConsRunner(cashBox));
            consumers[i].start();
        }
    }
}
