from time import sleep

from ocr import utils
from ocr.scanner.config import Scanner
from ocr.scanner.data import Box
from ocr.scanner.worker import Worker

config = Scanner


class BoxProcessor(Worker):
    """ Process for creating an instance of the Box class, which contains all obtained Frames and processed data. """
    sleep_time = .1

    def __init__(self, queue):
        super(BoxProcessor, self).__init__("Box-Processor", outputs=queue)
        self.box = None

    def init(self):
        self.box = None

    def new_box(self):
        self.box = Box()

    def finish_box(self):
        if self.box and self.box.frames:
            self.outputs.put(self.box)
        self.box = None

    def expire_box(self):
        if not self.box:
            return
        self.finish_box()

    def process(self, data):
        assert isinstance(data, list)

        if not self.box:
            self.new_box()

        for frame in data:
            self.box.add_frame(frame)

        if config.visualize:
            utils.show("Box-first frame", self.box.frames["front"][0].image)

    def run(self):
        self.init()
        while not self.terminating:
            self.expire_box()
            while True:
                data = self.inputs.get_default("nothing")
                if data is None:
                    self.terminate()
                    break
                if data == "nothing":
                    break
                self.process(data)

            if self.terminating:
                break
            sleep(self.sleep_time)
