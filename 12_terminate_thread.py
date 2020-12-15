"""Due to a global interpreter lock (GIL), Python threads are restricted to an execution
model that only allows one thread to execute in the interpreter at any given time. For
this reason, Python threads should generally not be used for computationally intensive
tasks where you are trying to achieve parallelism on multiple CPUs. They are much
better suited for I/O handling and handling concurrent execution in code that performs
blocking operations (e.g., waiting for I/O, waiting for results from a database, etc.).
"""
import time
from threading import Thread


class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print(n)
            n -= 1
            time.sleep(1)


c = CountdownTask()
t = Thread(target=c.run, args=(10,))
t.start()
time.sleep(5)
c.terminate()  # Signal termination
t.join()

time.sleep(5)
print('Main thread terminate')
