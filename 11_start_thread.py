"""The threading library can be used to execute any Python callable in its own thread. To
do this, you create a Thread instance and supply the callable that you wish to execute
as a target.
"""
import time
from threading import Thread


def coundown(n):
    while n > 0:
        print(n)
        n -= 1
        time.sleep(0.5)


t1 = Thread(target=coundown, args=(1000000,))
t1.start()
t2 = Thread(target=coundown, args=(10,))
t2.start()
