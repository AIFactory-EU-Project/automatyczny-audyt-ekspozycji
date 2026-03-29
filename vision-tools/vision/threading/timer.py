from threading import Thread
import time


class Timer(Thread):

    def __init__(self, func, timeout):
        super(Timer, self).__init__()
        self.func = func
        self.timeout = timeout
        self._canceled = False

    def run(self):
        while not self._canceled:
            t1 = time.time()
            self.func()
            t2 = time.time()
            time.sleep(max(0, self.timeout - (t2 - t1)))

    def stop(self):
        self._canceled = True
