# script to create lists of train, validate and test values

import os
import random
import re

PARTITION_FILE = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/Eval/list_eval_partition.txt"
INPUT_DIR = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/"
TRAIN_FILE = "/tytan/raid/fashion/detection/lmdb/deepfashion/train.txt"
TEST_FILE = "/tytan/raid/fashion/detection/lmdb/deepfashion/test.txt"
DEMO_FILE = "/tytan/raid/fashion/detection/lmdb/deepfashion/demo.txt"

with open(PARTITION_FILE, 'r') as part_file, open(DEMO_FILE, 'w') as demo_file, open(TRAIN_FILE, 'w') as train_file, open(TEST_FILE, 'w') as test_file:
    train_imgs = []
    test_imgs = []
    demo_imgs = []

    lines = part_file.read().splitlines()
    n = int(lines[0])
    for i in range(n):
        line = lines[i + 2]
        line = re.sub(' +', ' ', line)
        img_path, action = line.split(' ')
        anno_path = "Anno/" + os.path.join(*(img_path.split(os.path.sep)[1:]))
        anno_path = os.path.splitext(anno_path)[0] + ".xml"

        row = "{0} {1}".format(img_path, anno_path)
        if action == "train":
            train_imgs.append(row)
        elif action == "val":
            train_imgs.append(row)
        else:
            test_imgs.append(row)
            demo_imgs.append("{0}{1}".format(INPUT_DIR, img_path))

        if i % 1000 == 0:
            print("Processed {0}/{1}".format(i, n))

    train_file.write("\n".join(train_imgs))
    test_file.write("\n".join(test_imgs))

    random.shuffle(demo_imgs)
    demo_file.write("\n".join(demo_imgs))
