'''In multithreaded programs, a common source of deadlock is due to threads that attempt
to acquire multiple locks at once. For instance, if a thread acquires the first lock, but
then blocks trying to acquire the second lock, that thread can potentially block the
progress of other threads and make the program freeze.
One solution to deadlock avoidance is to assign each lock in the program a unique
number, and to enforce an ordering rule that only allows multiple locks to be acquired
in ascending order.
The key to this recipe lies in the first statement that sorts the locks according to object
identifier. By sorting the locks, they always get acquired in a consistent order regardless
of how the user might have provided them to acquire().
'''
import threading
from contextlib import contextmanager

_local = threading.local()


@contextmanager
def acquire(*locks):
    locks = sorted(locks, key=lambda x: id(x))

    acquired = getattr(_local, 'acquired', [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('Lock Order Violation')

    # Acquire all of the locks
    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        # Release locks in reverse order of acquisition
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]


x_lock = threading.Lock()
y_lock = threading.Lock()


def thread_1():
    while True:
        with acquire(x_lock, y_lock):
            print('Thread-1')


def thread_2():
    while True:
        with acquire(y_lock, x_lock):
            print('Thread-2')


t1 = threading.Thread(target=thread_1)
t1.daemon = True
t1.start()
t2 = threading.Thread(target=thread_2)
t2.daemon = True
t2.start()
