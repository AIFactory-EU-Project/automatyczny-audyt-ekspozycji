# script to compute accuracy of deepfashion detection with ignored boxes

import re

import cv2
import six

from vision.caffe.fashion.detect import ClothesDetector

DEMO_FILE = "/tytan/raid/fashion/detection/lmdb/deepfashion/demo.txt"
LABELS_FILE = "/tytan/raid/fashion/detection/lmdb/deepfashion/demo_label.txt"

detector = ClothesDetector()

lines = []
with open(DEMO_FILE, 'r') as demo_file:
    lines = demo_file.read().splitlines()

results = {}
labels = []
with open(LABELS_FILE, 'r') as label_file:
    tmp = label_file.read().splitlines()
    for t in tmp:
        _, l = t.split(' ')
        labels.append(l)

for label in labels:
    results[label] = {"tp": 0,
                      "tn": 0,
                      "fp": 0,
                      "fn": 0}

for i, path in enumerate(lines):
    img = cv2.imread(path)
    boxes = detector.get_result(img)
    clothes = [x[0] for x in boxes]

    anno_path = path.replace("/img/", "/Anno/xml/").replace(".jpg", ".xml")
    with open(anno_path, 'r') as anno_file:
        content = anno_file.read()
        pattern = re.compile("<name>(.*)</name>\n")
        ground_truth = [pattern.search(content).group(1)]

    for label in labels:
        if label in ground_truth and label in clothes:
            results[label]["tp"] += 1
        elif label not in ground_truth and label not in clothes:
            results[label]["tn"] += 1
        elif label not in ground_truth and label in clothes:
            results[label]["fp"] += 1
        else:
            results[label]["fn"] += 1

    if i % 1000 == 0:
        print("{}/{}".format(i, len(lines)))

for k, v in six.iteritems(results):
    print(k, v["tp"], v["tn"], v["fp"], v["fn"])

detector.shutdown()
