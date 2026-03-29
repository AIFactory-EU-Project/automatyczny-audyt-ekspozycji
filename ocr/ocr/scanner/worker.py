import logging
import multiprocessing

from multiprocessing import Process
from multiprocessing.queues import Queue
from queue import Empty

from vision.helpers.misc import time_it


class Queue(Queue):
    def __init__(self):
        super().__init__(ctx=multiprocessing.get_context())

    def get_default(self, default=None):
        try:
            return self.get_nowait()
        except Empty:
            return default


class Worker(Process):
    def __init__(self, name, inputs=None, outputs=None):
        super(Worker, self).__init__()
        self.daemon = True
        self.terminating = False
        self.name = name
        self.inputs = inputs or Queue()
        self.outputs = outputs or Queue()
        self.start()

    def init(self):
        pass

    def run(self):
        self.init()
        logging.debug("{} ready".format(self.name))
        while not self.terminating:
            data = self.inputs.get()
            if data is None or self.terminating:
                self.terminate()
                break
            with time_it(self.name):
                output = self.process(data)
            self.outputs.put(output)

    def process(self, data):
        return None

    def terminate(self):
        logging.debug("Terminating {}".format(self.name))
        self.terminating = True
        self.inputs.put(None)
        self.outputs.put(None)
