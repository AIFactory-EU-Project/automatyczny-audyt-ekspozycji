import logging
import math

from multiprocessing import Queue
from datetime import datetime

from ocr.scanner.data import Frame
from ocr.scanner.worker import Worker
from vision.helpers.misc import time_it


class Camera(Worker):
    """ Process for detecting boxes on the images obtained from the camera. """
    sleep_time = 1000000

    def __init__(self, name, queue, images, batch_size=5):
        self.name = name
        self.images_queue = Queue()
        max_iters = int(math.ceil(len(images) / batch_size))
        start = 0
        for i in range(max_iters):
            if i == max_iters - 1:
                img_batch = images[start:]
            else:
                img_batch = images[start:start + batch_size]
            self.images_queue.put(img_batch)

        super(Camera, self).__init__("Camera-" + name, outputs=queue)

    def init(self):
        # self.detector = BoxDetector(self.images)
        pass

    def run(self):
        self.init()

        while not self.terminating:
            t = time_it(self.name)
            t.start()
            frames = []
            images = self.images_queue.get()
            if not images:
                self.terminate()
                return

            for img in images:
                timestamp = datetime.now()
                # aligned = self.detector.detect(img)
                aligned = img
                if aligned is not None:
                    frame = Frame(timestamp, img, self.name.split("-")[1])
                    frame.aligned = aligned
                    frames.append(frame)
            self.outputs.put(frames)
            t.stop()

        logging.debug("End {}".format(self.name))
