import time
import os
import glob
import cv2
import numpy as np

from datetime import datetime

from ocr.scanner.aocr import Ocr
from ocr.scanner.boxes import BoxProcessor
from ocr.scanner.camera import Camera
from ocr.scanner.config import Scanner
from ocr.scanner.barcodes import BarcodeReader
from ocr.scanner.data import Box
from ocr.scanner.detector import Detector
from ocr.scanner.parser import TextParser
from ocr.scanner.worker import Queue
from vision.helpers.image_helpers import fit_to_size

SHOW = True

TEXT_THRESHOLD = 0

config = Scanner


def get_images_for_camera(imgs_pth):
    images = []
    for img_pth in glob.iglob(os.path.join(imgs_pth, "**/*.jpg"), recursive=True):
        images.append(cv2.imread(img_pth))
    return images


class Master(object):
    """ Main process for processing, gathering and presenting results. """
    def __init__(self, screen_resolution):
        self.boxes = Queue()
        self.parser = TextParser(self.boxes)
        self.ocr = Ocr(self.parser.inputs)
        time.sleep(3)
        self.detector = Detector(self.ocr.inputs)
        self.barcode_reader = BarcodeReader(self.detector.inputs)
        self.box_processor = BoxProcessor(self.barcode_reader.inputs)
        self.img_width = screen_resolution[0]
        self.img_height = screen_resolution[1]
        self.cameras = {name: Camera(name, self.box_processor.inputs, get_images_for_camera(cfg.images_pth))
                        for name, cfg in config.cameras.items()}
        self.num_of_windows = config.num_of_windows

    def start(self):
        act_window = 0
        img_size = (int(self.img_width * 0.33), int(self.img_height * 0.45))
        front_size = (int(self.img_width * 0.33), int(self.img_height * 0.45))
        detections_size = (int(self.img_width * 0.33), int(self.img_height * 0.66))
        results_size = (int(self.img_width * 0.33), int(self.img_height * 0.33))

        img_pos = (0, 30)
        front_pos = (img_size[0] + 5, 30)
        results_pos = (img_size[0] + front_size[0] + 10, 30)
        detections_pos = (results_pos[0], results_size[1] + 60)

        try:
            while True:
                box = self.boxes.get()
                if box is None:
                    self.terminate()
                    break

                assert isinstance(box, Box)

                frame = box.one_frame()
                print("Box processed. Time: {}".format(datetime.now() - frame.timestamp))
                print(box)

                if SHOW:
                    image = frame.image.copy()
                    front = frame.aligned.copy()
                    detections = np.zeros((detections_size[1], detections_size[0], 3), dtype=np.uint8)
                    results = np.zeros((results_size[1], results_size[0], 3), dtype=np.uint8)
                    det_width = detections_size[0] / 2
                    det_height = 80

                    y = 0
                    for idx, detection in enumerate([frame.barcode] + frame.detections):
                        if not detection.text or detection.text_confidence < TEXT_THRESHOLD:
                            if detection.x1:
                                cv2.rectangle(front, (detection.x1, detection.y1), (detection.x2, detection.y2), (128, 128, 255, 0), 1)
                            continue

                        ocr = detection.image(margin=8)
                        if ocr.shape[0] > ocr.shape[1]:
                            ocr = np.rot90(ocr, 3)

                        ocr = fit_to_size(ocr, (det_width, det_height))
                        text = "[{:.2f}] [{:.2f}] {}".format(detection.confidence, detection.text_confidence, detection.text)

                        if image.shape[0] > y + ocr.shape[0] and image.shape[1] > ocr.shape[1]:
                            q = detections[y:y + ocr.shape[0], 0:ocr.shape[1], ...]
                            if q.shape != ocr.shape:
                                # fixme: dupiasty workaround - nigdy nie powinnismy tu byc!
                                print("WARN wrong ocr shape")
                                continue
                            detections[y:y + ocr.shape[0], 0:ocr.shape[1], ...] = ocr
                            cv2.rectangle(front, (detection.x1, detection.y1), (detection.x2, detection.y2), (0, 255, 0, 0), 2)
                            cv2.putText(detections, text, (int(det_width) + 2, y + int(det_height / 2)), 1, 1, (255, 255, 255, 0), 1, cv2.LINE_AA)
                            y += det_height + 2

                    txt = "Barcode:         {}".format(box.barcode or "---")
                    cv2.putText(results, txt, (0, 50), 2, 1, (255, 255, 255, 0), 2, cv2.LINE_AA)

                    txt = "   Serial: [{:.2f}] {}".format(box.serial_number_score, box.serial_number or "---")
                    cv2.putText(results, txt, (0, 100), 2, 1, (255, 255, 255, 0), 2, cv2.LINE_AA)

                    txt = "    Date: [{:.2f}] {}".format(box.date_score, box.date or "---")
                    cv2.putText(results, txt, (0, 150), 2, 1, (255, 255, 255, 0), 2, cv2.LINE_AA)

                    image = fit_to_size(image, img_size)
                    front = fit_to_size(front, front_size)

                    cv2.imshow("Front {}".format(act_window), front)
                    cv2.imshow("Snapshot {}".format(act_window), image)
                    cv2.imshow("Text {}".format(act_window), detections)
                    cv2.imshow("Result {}".format(act_window), results)

                    cv2.moveWindow("Front {}".format(act_window), act_window * self.img_width + front_pos[0], front_pos[1])
                    cv2.moveWindow("Snapshot {}".format(act_window), act_window * self.img_width + img_pos[0], img_pos[1])
                    cv2.moveWindow("Text {}".format(act_window), act_window * self.img_width + detections_pos[0], detections_pos[1])
                    cv2.moveWindow("Result {}".format(act_window), act_window * self.img_width + results_pos[0], results_pos[1])

                    act_window = (act_window + 1) % self.num_of_windows

                    # waitKey()

        except KeyboardInterrupt:
            print("Keyboard interrupt")

        self.terminate()

    def terminate(self):
        print("Terminating all workers...")
        workers = self.cameras.values()
        for w in workers:
            w.terminate()
        print("Waiting for workers to finish...")
        for w in workers:
            w.join()
        print("All workers terminated.")
