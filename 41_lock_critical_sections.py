"""To make mutable objects safe to use by multiple threads, use Lock objects in the 
threading library, as shown here:
"""
import threading


class SharedCounter:
    # A counter object that can be shared by multiple threads.
    def __init__(self, initial_value=0):
        self._value = initial_value
        self._value_lock = threading.Lock()

    def incr(self, delta=1):
        # Increment the counter with locking
        with self._value_lock:
            self._value += delta

    def decr(self, delta=1):
        # Decrement the counter with locking
        with self._value_lock:
            self._value -= delta
