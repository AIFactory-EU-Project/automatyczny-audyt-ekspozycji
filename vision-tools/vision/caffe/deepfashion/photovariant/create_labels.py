# script to create lists of train, validate and test values
import os
import re

PARTITION_FILE = "/tytan/raid/fashion/data/deepfashion/InShopClothesRetrieval/Eval/list_eval_partition.txt"
INPUT_DIR = "/tytan/raid/fashion/data/deepfashion/InShopClothesRetrieval"
LABELS_FILE = "/tytan/raid/fashion/databases/deepfashion/photo-variant/labels.txt"
NAMES_FILE = "/tytan/raid/fashion/databases/deepfashion/photo-variant/names.txt"
ANNO_FILE = "/tytan/raid/fashion/data/deepfashion/InShopClothesRetrieval/Anno/list_bbox_inshop.txt"

POSE_LIST = ['front', 'side', 'back', 'zoom-out', 'zoom-in', 'stand-alone']

annotations = {}

with open(NAMES_FILE, 'w') as names_file:
    names_file.write("\n".join(POSE_LIST))

with open(ANNO_FILE) as anno_file:
    lines = anno_file.read().splitlines()
    n = int(lines[0])
    for i in range(n):
        line = lines[i + 2]
        line = re.sub(' +', ' ', line)
        path, _, pose = line.split(' ')[:3]
        annotations[path] = int(pose) - 1

with open(PARTITION_FILE, 'r') as part_file, open(LABELS_FILE, 'w') as labels_file:
    imgs = []

    lines = part_file.read().splitlines()
    n = int(lines[0])
    for i in range(n):
        line = lines[i + 2]
        line = re.sub(' +', ' ', line)
        img_path = line.split(' ')[0]

        row = "{0} {1}".format(os.path.join(INPUT_DIR, img_path), annotations[img_path])
        imgs.append(row)

        if i % 1000 == 0:
            print("Processed {0}/{1}".format(i, n))

    labels_file.write("\n".join(imgs))
