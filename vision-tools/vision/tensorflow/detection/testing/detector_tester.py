import cv2
import itertools
import numpy as np

from vision.helpers import box_helpers


def rect_from_quadrangle(quad):
    quad = np.array(quad)
    rect = cv2.boundingRect(quad)
    return rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]


def get_gt(json_data, key="products"):
    pairs = []
    for product in json_data[key]:
        rect = rect_from_quadrangle(product['coordinates'])
        pairs.append((1, rect))

    return pairs


def get_real_data(result):
    pairs = []
    for rect, score, class_no, _ in result:
        pairs.append((class_no, rect))
    return pairs


def connect_pairs(gt_pairs, result_pairs, dummy_pair=(0, (-1, -1, 0, 0))):
    result = []

    used_indexes = set()
    for gt_pair in gt_pairs:
        ious = np.array([box_helpers.bb_intersection_over_union(x[-1], y[-1]) for x, y in itertools.product([gt_pair], result_pairs)])
        max_iou = 0.0
        if ious.any():
            max_iou = np.max(ious)
        if max_iou > 0.5:
            i = int(np.argmax(ious))
            result.append((gt_pair, result_pairs[i]))
            used_indexes.add(i)
        else:
            result.append((gt_pair, dummy_pair))

    if len(result_pairs) > len(used_indexes):
        for i, pair in enumerate(result_pairs):
            if i not in used_indexes:
                result.append((dummy_pair, pair))

    return result


def compare(pairs, result):
    for gt, rd in pairs:
        assert not (gt[0] == rd[0] == 0), "ground true and real data can't be both 0"

        # this is very restrictive, if there is proper box, but with incorrect label it's fp and fn simultaneously
        keys = ["tp"] if gt[0] == rd[0] else ["fp"] if gt[0] == 0 else ["fn"] if rd[0] == 0 else ["fp", "fn"]

        for key in keys:
            result["displays"]["class"][key] += 1

        result["displays"]["boxes"].append(box_helpers.bb_intersection_over_union(gt[1], rd[1]))


def print_results(name, value, task="classification"):
    if not value["boxes"]:
        print()
        print("No boxes for {}".format(name))
        return

    boxes = np.array(value["boxes"])
    tp = value["class"]["tp"]
    fp = value["class"]["fp"]
    fn = value["class"]["fn"]
    accuracy = tp / (tp + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    fscore = 2 * precision * recall / (precision + recall)

    print("\n{} {} accuracy: {}".format(name, task, accuracy))
    print("{} {} precision: {}".format(name, task, precision))
    print("{} {} recall: {}".format(name, task, recall))
    print("{} {} fscore: {}".format(name, task, fscore))
    print("{} average IOU: {}".format(name, np.mean(boxes)))


def get_accuracy(value):
    tp = value["class"]["tp"]
    fp = value["class"]["fp"]
    fn = value["class"]["fn"]
    accuracy = tp / (tp + fp + fn)
    return accuracy


def print_whole_detections(number, total):
    print("Whole detections (no fp or fn in image): {}% {}/{}".format(number / total, number, total))


def show_results(img, result):
    for info, box in result:
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 5)
    cv2.imshow("image", img)
    cv2.waitKey()
