"""Although queues are the most common thread communication mechanism, you can
build your own data structures as long as you add the required locking and synchroni‐
zation. The most common way to do this is to wrap your data structures with a condition
variable. For example, here is how you might build a thread-safe priority queue
"""
import heapq
import threading


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._count = 0
        self._cv = threading.Condition()

    def put(self, item, priority):
        with self._cv:
            heapq.heappush(self._queue, (-priority, self._count, item))
            self._count += 1
            self._cv.notify()

    def get(self):
        with self._cv:
            while len(self._queue) == 0:
                self._cv.wait()
            return heapq.heappop(self._queue)[-1]
