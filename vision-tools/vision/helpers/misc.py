import threading
from datetime import datetime, timedelta


def roundint(f):
    return int(round(f))


class time_it(object):
    def __init__(self, msg=''):
        self.msg = "Time {}: {{:.4f}}s".format(msg)
        self.msg_sub = "Subtime {}: {{:.4f}}s".format(msg)
        self.started = None
        self.time = timedelta()

    def start(self):
        self.started = datetime.now()

    def stop(self, show=True):
        if self.started:
            self.pause()
        if show:
            print(self.msg.format(self.time.total_seconds()))

    def pause(self, show=False):
        t = datetime.now() - self.started
        self.time += t
        self.started = None
        if show:
            print(self.msg_sub.format(t.total_seconds()))

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def first_of(i):
    for a in i:
        return a


def length(o):
    if hasattr(o, "__len__"):
        return len(o)
    l = 0
    for _ in o:
        l += 1
    return l


def flattened(l):
    if hasattr(l, '__iter__'):
        for a in l:
            for x in flattened(a):
                yield x
    else:
        yield l


def nonempty(str_iter):
    for s in str_iter:
        s = s.rstrip()
        if s:
            yield s


class AtomicCounter(object):

    def __init__(self):
        self._lock = threading.Lock()
        self.value = 0

    def increment(self, value=1):
        with self._lock:
            self.value += value
            return self.value

    def decrement(self, value=1):
        with self._lock:
            self.value -= value
            return self.value

    def reset(self, value=0):
        with self._lock:
            self.value = value
            return self.value


def fourcc(s):
    assert len(s) == 4
    return ord(s[3]) << 24 | ord(s[2]) << 16 | ord(s[1]) << 8 | ord(s[0])


def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])
