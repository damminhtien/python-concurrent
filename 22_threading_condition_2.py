"""Event objects are best used for one-time events. That is, you create an event, threads
wait for the event to be set, and once set, the Event is discarded. Although it is possible
to clear an event using its clear() method, safely clearing an event and waiting for it
to be set again is tricky to coordinate, and can lead to missed events, deadlock, or other
problems (in particular, you can’t guarantee that a request to clear an event after setting
it will execute before a released thread cycles back to wait on the event again).
If a thread is going to repeatedly signal an event over and over, you’re probably better
off using a Condition object instead. For example, this code implements a periodic timer
that other threads can monitor to see whenever the timer expires:
"""
import threading
import time


class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()

    def run(self):
        '''
        Run the timer and notify waiting threads after each interval
        '''
        while True:
            time.sleep(self._interval)
            with self._cv:
                self._flag ^= 1
                self._cv.notify_all()

    def wait_for_tick(self):
        '''
        Wait for the next tick of the timer
        '''
        with self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()


ptimer = PeriodicTimer(5)
ptimer.start()


# Two threads that synchronize on the timer
def countdown(nticks):
    while nticks > 0:
        ptimer.wait_for_tick()
        print('T-minus', nticks)
        nticks -= 1


def countup(last):
    n = 0
    while n < last:
        ptimer.wait_for_tick()
        print('Counting', n)
        n += 1


threading.Thread(target=countdown, args=(10,)).start()
threading.Thread(target=countup, args=(5,)).start()
