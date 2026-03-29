import numpy as np

import cv2

TRAIN_FILE = "/tytan/raid/fashion/detection/lmdb/deepfashion/trainval.txt"
DATA_ROOT_DIR = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/"

with open(TRAIN_FILE, 'r') as train_file:
    mean = np.zeros(3, dtype=np.float64)
    lines = train_file.read().splitlines()
    n = len(lines)
    for i in range(n):
        line = lines[i]
        img_path, _ = line.split(' ')
        im = cv2.imread(DATA_ROOT_DIR + img_path)
        m = np.mean(np.mean(im, axis=0), axis=0) / n
        mean += m

        if i % 1000 == 0:
            print("Processed {0}/{1}".format(i, n))

    print(mean)
