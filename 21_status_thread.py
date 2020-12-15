"""Event instances are similar to a “sticky” flag that allows threads to wait for something
to happen. Initially, an event is set to 0. If the event is unset and a thread waits on the
event, it will block (i.e., go to sleep) until the event gets set. A thread that sets the event
will wake up all of the threads that happen to be waiting (if any). If a thread waits on an
event that has already been set, it merely moves on, continuing to execute.
"""
from threading import Thread, Event
import time


# Code to execute in an independent thread
def countdown(n, started_evt):
    started_evt.set()
    print('Countdown starting')
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)


# Create the event object that will be used to signal startup
started_evt = Event()
# Launch the thread and pass the startup event
print('Launching countdown')
t = Thread(target=countdown, args=(10, started_evt))
t.start()
# Wait for the thread to start
started_evt.wait()
print('Countdown is running')
