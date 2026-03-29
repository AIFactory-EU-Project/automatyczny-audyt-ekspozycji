import threading

import numpy as np


# https://keunwoochoi.wordpress.com/2017/08/24/tip-fit_generator-in-keras-how-to-parallelise-correctly/
class threadsafe_iter:
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """
    def __init__(self, it):
        self.it = it
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return self.it.__next__()


def threadsafe_generator(f):
    """A decorator that takes a generator function and makes it thread-safe.
    """
    def g(*a, **kw):
        return threadsafe_iter(f(*a, **kw))
    return g


class Generator:
    def __init__(self, batch_generator, data_file, input_size=(224, 224), batch_size=10, **kwargs):
        self.batch_gen = batch_generator(data_file, input_size, batch_size, **kwargs)

    @threadsafe_generator
    def next(self):
        while True:
            x_buffer, y_buffer = self.batch_gen.next_batch()
            yield np.array(x_buffer), np.array(y_buffer)
