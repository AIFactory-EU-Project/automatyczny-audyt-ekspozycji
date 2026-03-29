import cv2
import numpy as np

from zbar import zbar

from ocr.scanner.data import Detection
from ocr.scanner.worker import Worker


class BarcodeReader(Worker):
    """ Process for reading bar codes. """

    def __init__(self, queue):
        super(BarcodeReader, self).__init__("Barcode-Reader", outputs=queue)
        self.scanner = None

    def init(self):
        self.scanner = zbar.Scanner()

    def process(self, data):
        box = data
        for direction, box_frames in box.frames.items():
            for frame in box_frames:
                img = frame.aligned
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                barcodes = self.scanner.scan(img)

                if len(barcodes) > 0:
                    barcodes.sort(key=lambda x: (len(x.data), x.quality), reverse=True)
                    barcode = barcodes[0]
                    rect = cv2.boundingRect(np.array(barcode.position))
                    frame.barcode = Detection(frame, rect[0], rect[0] + rect[2], rect[1], rect[1] + rect[3], 1, barcode.data, 1)

        return box
