import itertools
import sys


class Pool(object):
    map = map
    imap = map if sys.version_info >= (3,0) else itertools.imap
    imap_unordered = imap
    _processes = 1

    def apply(self, function, args=(), kwargs={}):
        function(*args, **kwargs)

    def __init__(self, *a, **kw):
        pass

    def join(self):
        pass

ProcessPool = ThreadPool = Pool
