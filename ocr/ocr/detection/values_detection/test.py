import json
import os
import cv2

from collections import defaultdict
from tqdm import tqdm

from ocr.detection.values_detection.detector.detector import GCNetDetector
from vision.tensorflow.detection.testing import detector_tester as tester

SRC_PATH = "/tytan/raid/neuca/data/detection/values/balanced_legacy/annotations/validation.json"
CKPT_PATH = "/tytan/raid/neuca/models/detection/values/legacy/v1/epoch_4.pth"


def test(src_dir, ckpt_path, show=False):
    """
    Verify trained model on a test set.
    Currently only visual testing.

    :param src_dir: A path to the test directory.
    :param ckpt_path: A path to the trained model's checkpoint file.
    :param show: A boolean value to show detections.
    """
    detector = GCNetDetector(ckpt_path)

    with open(src_dir) as f:
        json_data = json.load(f)

    start = 0
    data_dict = defaultdict(list)
    for img_data in json_data["images"]:
        for anno_data in json_data["annotations"][start:]:
            if anno_data["image_id"] != img_data["id"]:
                break
            img_pth = os.path.join(os.path.dirname(os.path.dirname(src_dir)), os.path.basename(src_dir).split(".")[0], img_data["file_name"])
            data_dict[img_pth].append(anno_data["bbox"])
            start += 1

    final_results = {
        "values": {
            "class": {"tp": 0, "fp": 0, "fn": 0},
            "boxes": []
        },
    }

    for img_pth, annotations in tqdm(data_dict.items()):
        bboxes, labels = detector.predict(img_pth)

        gt_pairs = get_gt(annotations)
        img = cv2.imread(img_pth)

        result_pairs = []
        for bbox, label in zip(bboxes, labels):
            if label == 0:
                result_pairs.append((label, (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))))
                cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 255, 0))
                val1, val2 = gt_pairs
                val1, val2 = val1[1], val2[1]
                cv2.rectangle(img, (int(val1[0]), int(val1[1])), (int(val1[2]), int(val1[3])), (255, 0, 255))
                cv2.rectangle(img, (int(val2[0]), int(val2[1])), (int(val2[2]), int(val2[3])), (255, 0, 255))

        if show:
            print(img_pth)
            cv2.imshow("img", cv2.resize(img, None, fx=.5, fy=.5))
            cv2.waitKey(0)

        to_compare = tester.connect_pairs(gt_pairs, result_pairs, dummy_pair=(1, (-1, -1, 0, 0)))
        compare(to_compare, final_results)

    for k, v in final_results.items():
        tester.print_results(k.capitalize(), v, task="detection")


def get_gt(annotations):
    """
    Get ground truth data for a specific file.

    :param annotations: A list of lists containing bboxes in coco format.
    :return: A list of tuples (label, [coordinates]).
    """
    gt_pairs = []
    for anno in annotations:
        x, y, w, h = anno
        coords = (x, y, x + w, y + h)
        gt_pairs.append((0, coords))

    return gt_pairs


def compare(pairs, result):
    """
    Compare ground truth and real data. Calculate metrics.

    :param pairs: A list of tuples representing potential ground truth<->real data pairs.
    :param result: A result dict.
    """
    from vision.helpers.box_helpers import bb_intersection_over_union
    for gt, rd in pairs:
        # this is very restrictive, if there is proper box, but with incorrect label it's fp and fn simultaneously
        keys = ["tp"] if gt[0] == rd[0] else ["fp"] if gt[0] == 0 else ["fn"] if rd[0] == 0 else ["fp", "fn"]
        for key in keys:
            result["values"]["class"][key] += 1

        result["values"]["boxes"].append(bb_intersection_over_union(gt[1], rd[1]))


if __name__ == '__main__':
    test(SRC_PATH, CKPT_PATH, show=False)
