from threading import Event, Thread
from queue import Queue
from time import sleep


def get_task(args):
    event = Event()
    fila = Queue(maxsize=101)
    [fila.put(a) for a in args]
    event.set()
    return fila, event


class Worker(Thread):
    def __init__(self, target, queue, *, name='Worker ', event=None):
        super().__init__()
        self.name = name
        self.queue = queue
        self.event = event
        self._target = target
        self._stoped = False
        
    def run(self):
        self.event.wait()
        task_coin = self.queue.get()
        # print(f"\n{self.name}\n{task_coin}")
        self._target(task_coin)
        self._stoped = True
        
    def join(self):
        while not self._stoped:
            sleep(0.1)


def get_pool(n_th: int, target, queue=None, event=None):
    """Retorna um número n de Threads."""
    return [Worker(target=target, queue=queue, name=f'Worker{n}', event=event)
            for n in range(n_th)]

def teste(test):
    print(f"\nEste é um teste: {test}")
    sleep(1)

if __name__ == "__main__":
    coins = ["BTCUSDT", "BNBUSDT", "BTCBUSD"]
    fila, event = get_task(coins)
    print(fila.queue)
    thrs = get_pool(len(coins), target=teste, queue=fila, event=event)
    [th.start() for th in thrs]
    [th.join() for th in thrs]
