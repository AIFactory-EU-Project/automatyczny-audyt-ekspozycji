import numpy as np

from collections import defaultdict
from datetime import datetime, timedelta
from itertools import product

from vision.helpers.misc import time_it


class Detection(object):
    """ Represents ROI found by dates and serial numbers' detector as well as data read from it. """
    def __init__(self, frame, x1=None, x2=None, y1=None, y2=None, confidence=0, text="", text_confidence=0):
        self.frame = frame
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.confidence = confidence
        self.text = text
        self.text_confidence = text_confidence

    def image(self, margin=0, rotation=0):
        h, w, _ = self.frame.aligned.shape
        x1 = max(self.x1 - margin, 0)
        x2 = min(self.x2 + margin, w)
        y1 = max(self.y1 - margin, 0)
        y2 = min(self.y2 + margin, h)

        image = self.frame.aligned[y1:y2,x1:x2,...]
        image = np.rot90(image, rotation//90)
        return image

    def possible_orientations(self):
        w = self.x2 - self.x1
        h = self.y2 - self.y1
        horiz = float(w)/h > 0.8
        verti = float(h)/w > 0.8
        return horiz, verti


class Frame(object):
    """ Represents single image from the specified camera. """
    def __init__(self, timestamp, image, direction):
        self.timestamp = timestamp
        self.image = image  # original image
        self.aligned = None  # ROI containing box (found by box detector)
        self.direction = direction  # camera orientation (e.g. front, left)
        self.detections = []
        self.barcode = Detection(self)


class Box(object):
    """ Represents box on the image. """
    def __init__(self):
        self.timestamp = datetime.now()
        self.frames = defaultdict(list)  # direction -> list of frames
        self.date = ""
        self.serial_number = ""
        self.barcode = ""
        self.date_score = 0
        self.serial_number_score = 0
        self.timers = {}
        self.time = timedelta()

    def timer(self, name):
        if name not in self.timers: self.timers[name] = time_it(name)
        return self.timers[name]

    def add_frame(self, frame):
        self.frames[frame.direction].append(frame)

    def all_ocr_images(self):
        images = []
        detections = []
        for direction, box_frames in self.frames.items():
            for frame in box_frames:
                for detection in frame.detections:
                    horiz, verti = detection.possible_orientations()
                    margins = [0, 8, 16]
                    rotations = [0] * horiz + [90] * verti

                    for margin, rotation in product(margins, rotations):
                        detections.append(detection)
                        images.append(detection.image(margin, rotation))

        return detections, images

    def one_frame(self):
        if "front" in self.frames.keys():
            return self.frames["front"][0]
        if "left" in self.frames.keys():
            return self.frames["left"][0]

        raise Exception("No frames")

    def __repr__(self):
        t = u"Box:\n"
        t += "\ttimestamp: {}\n".format(self.timestamp)
        t += "\tprocessing time: {}\n".format(self.time)
        t += "\tdate: {}\n".format(self.date)
        t += "\tserial: {}\n".format(self.serial_number)
        t += "\tbarcode: {}\n".format(self.barcode)
        for direction, box_frames in self.frames.items():
            for frame in box_frames:
                t += "\tframe {}:\n".format(direction)
                t += "\t\ttimestamp: {}\n".format(frame.timestamp)
                for detection in sorted([frame.barcode] + frame.detections, key=lambda d: -d.confidence-d.text_confidence):
                    t += "\t\tdetection:\n"
                    if detection.x1 is not None:
                        t += "\t\t\tlocation: {}-{} {}-{}\n".format(detection.x1, detection.x2, detection.y1, detection.y2)
                    if detection.confidence is not None:
                        t += "\t\t\tconfidence: {:.3%}\n".format(detection.confidence)
                    if detection.text is not None:
                        t += "\t\t\ttext: {}\n".format(detection.text)
                    if detection.text_confidence is not None:
                        t += "\t\t\ttext confidence: {:.3%}\n".format(detection.text_confidence)
        return t
