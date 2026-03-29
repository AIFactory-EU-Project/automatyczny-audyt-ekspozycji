import cv2
import logging

from ocr import utils
from ocr.scanner.config import Scanner
from ocr.scanner.data import Box, Frame
from ocr.scanner.worker import Worker
from vision.tensorflow.gpus import tensorflow_use_gpus

config = Scanner


class Ocr(Worker):
    """ Process for OCR. """
    checkpoint = r"/kolos/m2/ocr/aocr/training/all-chars-aug13-updown/"
    custom_confidence = (5, 20)
    batch_size = 8

    def __init__(self, queue):
        super(Ocr, self).__init__("ocr", outputs=queue)
        self.ocr = None

    def init(self):
        tensorflow_use_gpus(1)
        from vision.aocr.api import AOCR
        import tensorflow as tf

        config = tf.ConfigProto()
        config.gpu_options.per_process_gpu_memory_fraction = 0.1
        tf.Session(config=config).as_default()
        self.ocr = AOCR(self.checkpoint, batch_size=self.batch_size, custom_confidence=self.custom_confidence)

    def process(self, data):
        box = data
        assert isinstance(box, Box)

        logging.debug("Reading data from the box...")

        with box.timer("All_ocr_images"):
            detections, images = box.all_ocr_images()
        with box.timer("Ocr predict"):
            results = self.ocr.predict(images)
        for i, (text, confidence) in enumerate(results):
            detection = detections[i]

            if len(text.replace(" ", "").replace("*", "")) < 3:
                confidence = 0

            if confidence >= detection.text_confidence:
                detection.text, detection.text_confidence = text, confidence

            if config.visualize:
                print("frame", detection.frame, "text", detection.text, "confidence", detection.text_confidence)
                preview = cv2.resize(images[i], (0, 0), fx=4, fy=4)
                cv2.putText(preview, str(text), (10, 20), 1, 1, 0, 1, cv2.LINE_AA)
                cv2.putText(preview, str(confidence), (10, 40), 1, 1, 0, 1, cv2.LINE_AA)
                utils.show("Recognized text {}".format(i), preview)

        with box.timer("Ocr sorting"):
            for direction, box_frames in box.frames.items():
                for frame in box_frames:
                    assert isinstance(frame, Frame)
                    frame.detections.sort(key=lambda f: -f.confidence - f.text_confidence)

        return box
