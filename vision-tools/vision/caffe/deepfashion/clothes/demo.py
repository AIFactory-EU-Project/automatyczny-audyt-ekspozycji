# shows image with class and bounding box
import os
import re
import subprocess

import cv2

DETECT_BIN = "/home/tytan/caffe-ssd/build/examples/ssd/ssd_detect.bin"
ARGS = "-mean_value \"180, 183, 192\""
NET_MODEL = "/home/tytan/caffe-ssd/models/VGGNet/deepfashion/SSD_300x300/deploy.prototxt"
TRAINED_NET = "/home/tytan/caffe-ssd/models/VGGNet/2deepfashion/SSD_300x300/VGG_DEEPFASHION_SSD_300x300_iter_500000.caffemodel"
TEST_FILE = "/tytan/raid/fashion/detection/lmdb/deepfashion/demo_amazon.txt"
INPUT_DIR = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/img"
LABEL_FILE = "/tytan/raid/fashion/detection/lmdb/deepfashion/demo_label.txt"

RESIZE_TO = 600

COLORS = ((0, 0, 255),
          (0, 255, 0),
          (255, 0, 0),
          (0, 255, 255),
          (255, 255, 0),
          (255, 0, 255),
          (128, 128, 128))

labels = {}
with open(LABEL_FILE, 'r') as label_file:
    lines = label_file.read().splitlines()
    for line in lines:
        num, cat = line.split(' ')
        labels[int(num)] = cat

proc = subprocess.Popen(" ".join([DETECT_BIN, ARGS, NET_MODEL, TRAINED_NET, TEST_FILE]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
prev_line_path = ""
cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
im = None
boxes = []

for line in proc.stdout:
    if re.match("/tytan/raid/fashion/data/.*", line):
        path, cat, acc, x1, y1, x2, y2 = line.replace("\n", "").split(' ')
        if prev_line_path != path:
            if prev_line_path != "":
                im = cv2.imread(prev_line_path)
                for i, box in enumerate(boxes):
                    cv2.rectangle(im, box[2:4], box[4:], COLORS[i % len(COLORS)], im.shape[0] // 300)

                scale_ratio = float(RESIZE_TO) / max(im.shape[0], im.shape[1])
                im = cv2.resize(im, dsize=None, fx=scale_ratio, fy=scale_ratio)
                im = cv2.copyMakeBorder(im, 20 * (len(boxes) + 1), 0, 0, 0, cv2.BORDER_CONSTANT)
                for i, box in enumerate(boxes):
                    cv2.putText(im, "{}:  {}".format(labels[box[0]], box[1]), (15, 20 * (i + 1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[i % len(COLORS)], 1)
                    print(os.path.basename(prev_line_path), ":", labels[box[0]], box[1])

                print("------------------------------------------------------------------------------------------------")
                cv2.imshow("demo", im)
                cv2.waitKey(0)
            prev_line_path = path
            boxes = []
        if float(acc) > 0.3:
            boxes.append((int(cat), acc, int(x1), int(y1), int(x2), int(y2)))

        print(path, labels[int(cat)], acc, x1, y1, x2, y2)
