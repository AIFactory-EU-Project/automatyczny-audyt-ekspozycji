import logging
import cv2
import numpy as np

from ocr import utils
from ocr.scanner.config import Scanner
from ocr.scanner.data import Box, Detection
from ocr.scanner.worker import Worker

from vision.tensorflow.gpus import tensorflow_use_gpus

config = Scanner


class Detector(Worker):
    """ Process for date and serial number's localisation """
    def __init__(self, queue):
        super(Detector, self).__init__("detector", outputs=queue)
        self.detector = None

    def init(self):
        tensorflow_use_gpus(1)
        from ocr.detection.values_detection.detector.detector import GCNetDetector
        self.detector = GCNetDetector("/tytan/raid/neuca/models/detection/values/v1/latest.pth",
                                      "../detection/values_detection/detector/gcnet.py")

    def process(self, data):
        assert isinstance(data, Box)

        logging.debug("Detecting serials and dates on the box...")
        box = data
        for direction, box_frames in box.frames.items():
            for box_frame in box_frames:
                frames = []
                images = []
                frames.append(box_frame)
                frames.append(box_frame)
                image = np.array(box_frame.aligned)
                images.append(image)
                images.append(cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE))
                results = self.detector.predict(images)
                results_l = list(results)

                if config.visualize:
                    from object_detection.utils import visualization_utils as vis_util
                    img = images[1]
                    boxes, scores, classes, num = results_l[1]
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        img, boxes, classes, scores, self.detector.category_index,
                        use_normalized_coordinates=True,
                        line_thickness=2,
                        min_score_thresh=self.detector.detection_threshold)
                    utils.show("Detection", img)

                detected_boxes = 0
                for i, (frame, result) in enumerate(zip(frames, results_l)):
                    bboxes, labels = result

                    for bbox in bboxes:
                        score = bbox[4]
                        if score < self.detector.detection_threshold:
                            continue

                        detected_boxes += 1

                        image = frame.aligned
                        im_height, im_width = image.shape[:2]
                        xmin, ymin, xmax, ymax = bbox[:4]
                        # rotated image
                        if i % 2:
                            tmp_y1 = ymin
                            tmp_y2 = ymax
                            ymin = xmin
                            ymax = xmax
                            xmin = im_width - tmp_y1
                            xmax = im_width - tmp_y2

                        xmin = max(0, int(xmin))
                        ymin = max(0, int(ymin))
                        xmax = min(im_width, int(xmax))
                        ymax = min(im_height, int(ymax))

                        # img = image.copy()
                        # cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 255, 0))
                        # cv2.imshow("img", cv2.resize(img, None, fx=.5, fy=.5))
                        # cv2.waitKey()

                        detection = Detection(frame, xmin, xmax, ymin, ymax, score)
                        frame.detections.append(detection)

        return box
