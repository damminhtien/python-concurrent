"""A critical feature of Event objects is that they wake all waiting threads. If you are writing
a program where you only want to wake up a single waiting thread, it is probably better
to use a Semaphore or Condition object instead.
"""
import threading
import time


# Worker thread
def worker(n, sema):
    # Wait to be signaled
    sema.acquire()
    # Do some work
    print('Working', n)
    sema.release()


# Create some threads
sema = threading.Semaphore(0)
nworkers = 10
for n in range(nworkers):
    t = threading.Thread(target=worker, args=(n, sema,))
    t.start()
sema.release()
