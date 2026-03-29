import time
import json
import cv2
import editdistance
import numpy as np

from ocr.scanner.aocr import Ocr
from ocr.scanner.boxes import BoxProcessor
from ocr.scanner.camera import Camera
from ocr.scanner.barcodes import BarcodeReader
from ocr.scanner.detector import Detector
from ocr.scanner.parser import TextParser
from ocr.scanner.worker import Queue

SRC = "/tytan/raid/neuca/data/orig/tagger_data/1/annotations.json"


def rotate_bound(img, angle):
    im_height, im_width = img.shape[:2]
    center_x, center_y = im_width // 2, im_height // 2
    mtx = cv2.getRotationMatrix2D((center_x, center_y), -angle, 1.0)

    cos = np.abs(mtx[0, 0])
    sin = np.abs(mtx[0, 1])
    new_width = int((im_height * sin) + (im_width * cos))
    new_height = int((im_height * cos) + (im_width * sin))
    # adjust rotation matrix to take translation into account
    mtx[0, 2] += (new_width / 2) - center_x
    mtx[1, 2] += (new_height / 2) - center_y

    img = cv2.warpAffine(img, mtx, (new_width, new_height), flags=cv2.INTER_LINEAR)
    return img


def get_gt(json_data):
    gt = []
    for entry in json_data:
        img = cv2.imread(entry["localPath"])
        angle = entry["boxArea"]["rotate"]
        if angle:
            img = rotate_bound(img, angle)
        box_area = entry["boxArea"]
        x, y = max(0, box_area["x"]), max(0, box_area["y"])
        w, h = box_area["width"], box_area["height"]
        img = img[y:y+h, x:x+w]
        gt.append((img, entry["dateText"], entry["seriesText"]))

    return gt


def test_barcodes(gt, recognized):
    edit_dist = editdistance.eval(gt, recognized)
    return 1.0 - float(edit_dist) / max(len(gt), len(recognized))


def test_date_and_serials(gt, recognized):
    edit_dist = editdistance.eval(gt, recognized)
    return 1.0 - float(edit_dist) / max(len(gt), len(recognized))


def test_box(date_txt, series_txt, res_dates, res_serials, box=None):
    zero_vec = [0.0, 0.0]
    if box:
        acc_date = test_date_and_serials(date_txt, box.date) if date_txt else None
        acc_sn = test_date_and_serials(series_txt, box.serial_number) if series_txt else None
    if date_txt:
        res_dates.append([1.0 if acc_date == 1.0 else 0.0, acc_date] if box else zero_vec)
    if series_txt:
        res_serials.append([1.0 if acc_sn == 1.0 else 0.0, acc_sn] if box else zero_vec)


def test(src):
    boxes = Queue()
    parser = TextParser(boxes)
    ocr = Ocr(parser.inputs)
    time.sleep(3)
    detector = Detector(ocr.inputs)
    barcode_reader = BarcodeReader(detector.inputs)
    box_processor = BoxProcessor(barcode_reader.inputs)

    with open(src, "r") as f:
        json_data = json.load(f)

    gt = get_gt(json_data)
    camera = Camera("front", box_processor.inputs, [])

    results_dates = []
    results_serials = []
    i = 0
    while True:
        img, date_txt, series_txt = gt[i]
        camera.images_queue.put([img])
        box = boxes.get()
        if box is None:
            break
        test_box(date_txt, series_txt, results_dates, results_serials, box)
        i += 1

    if results_dates:
        avg_dates = np.mean(np.array(results_dates), axis=0)
        print("AVG whole accuracy for dates: ", avg_dates[0])
        print("AVG accuracy for dates", avg_dates[1])
    if results_serials:
        avg_serials = np.mean(np.array(results_serials), axis=0)
        print("AVG whole accuracy for serial numbers: ", avg_serials[0])
        print("AVG accuracy for serial numbers", avg_serials[1])


if __name__ == '__main__':
    test(SRC)
