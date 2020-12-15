"""Perhaps the safest way to send data from one thread to another is to use a Queue 
from the queue library. We create a Queue instance that is shared by the threads.
Threads then use put() or get() operations to add or remove items from the queue.
---
When using queues, it can be somewhat tricky to coordinate the shutdown of the pro‐
ducer and consumer. A common solution to this problem is to rely on a special sentinel
value, which when placed in the queue, causes consumers to terminate.
---
Thread communication with a queue is a one-way and nondeterministic process. In
general, there is no way to know when the receiving thread has actually received a
message and worked on it. However, Queue objects do provide some basic completion
features, as illustrated by the task_done() and join() methods
---
One caution with thread queues is that putting an item in a queue doesn’t make a copy
of the item. Thus, communication actually involves passing an object reference between
threads. If you are concerned about shared state, it may make sense to only pass im‐
mutable data structures (e.g., integers, strings, or tuples) or to make deep copies of the
queued items. out_q.put(copy.deepcopy(data))
"""
from queue import Queue
from threading import Thread
import random
import time


# Object that signals shutdown
_sentinel = object()


# A thread that produces data
def producer(out_q):
    while True:
        time.sleep(0.01)
        # Produce some data
        data = random.randint(0, 10)
        print('Produce data', data)
        out_q.put(data)
    # Put the sentinel on the queue to indicate completion
    out_q.put(_sentinel)


# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()
        print('Receive data', data)

        # Check for termination
        if data is _sentinel:
            in_q.put(_sentinel)
            break

        # Indicate completion
        in_q.task_done()


# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()
# Wait for all produced items to be consumed
q.join()

