import os
import re
from shutil import copyfile

INPUT_FILE = "/tytan/raid/fashion/data/deepfashion/InShopClothesRetrieval/Anno/list_bbox_inshop.txt"
OUTPUT_DIR = "/tytan/raid/fashion/data/deepfashion/photo-variant"
SET_ROOT_DIR = "/tytan/raid/fashion/data/deepfashion/InShopClothesRetrieval"
BY_NAME_DIR = os.path.join(OUTPUT_DIR, "by-name")
BY_POSE_DIR = os.path.join(OUTPUT_DIR, "by-pose")

NAMES_LIST = ['additional', 'back', 'flat', 'front', 'full', 'side']

POSE_MAP = {'1': 'frontal',
            '2': 'side',
            '3': 'back',
            '4': 'zoom-out',
            '5': 'zoom-in',
            '6': 'stand-alone'}

for name in NAMES_LIST:
    if not os.path.exists(os.path.join(BY_NAME_DIR, name)):
        os.makedirs(os.path.join(BY_NAME_DIR, name))

for label in POSE_MAP.values():
    if not os.path.exists(os.path.join(BY_POSE_DIR, label)):
        os.makedirs(os.path.join(BY_POSE_DIR, label))

with open(INPUT_FILE) as labels_file:
    lines = labels_file.read().splitlines()
    n = int(lines[0])
    for i in range(n):
        line = lines[i + 2]
        line = re.sub(' +', ' ', line)
        path, _, pose = line.split(' ')[:3]
        copyfile(os.path.join(SET_ROOT_DIR, path), os.path.join(BY_POSE_DIR, POSE_MAP[pose], (str(i) + '_' + os.path.basename(path))))
        name = os.path.splitext(os.path.basename(path))[0].split('_')[2]
        copyfile(os.path.join(SET_ROOT_DIR, path), os.path.join(BY_NAME_DIR, name, (str(i) + '_' + os.path.basename(path))))
        if i % 1000 == 0:
            print("Processed {0}/{1}".format(i, n))
