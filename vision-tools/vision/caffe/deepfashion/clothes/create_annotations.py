# script to create annotation files for deep fashion dataset

import os
import re
from PIL import Image

CATEGORY_FILE = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/Anno/list_category_cloth.txt"
IMAGE_FILE = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/Anno/list_category_img.txt"
BBOX_FILE = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/Anno/list_bbox.txt"
INPUT_DIR = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/"
OUTPUT_DIR = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/Anno/"


TEMPLATE ="""<annotation>
    <size>
        <width>{0}</width>
        <height>{1}</height>
        <depth>3</depth>
    </size>
    <object>
        <name>{2}</name>
        <bndbox>
            <xmin>{3}</xmin>
            <ymin>{4}</ymin>
            <xmax>{5}</xmax>
            <ymax>{6}</ymax>
        </bndbox>
    </object>
</annotation>"""

categories = {}

# get possible categories
with open(CATEGORY_FILE, 'r') as cat_file:
    img_lines = cat_file.read().splitlines()
    n = int(img_lines[0])
    for i in range(n):
        img_line = img_lines[i + 2]
        img_line = re.sub(' +', ' ', img_line)
        cat, _ = img_line.split(' ')
        categories[i + 1] = cat


with open(IMAGE_FILE, 'r') as list_file, open(BBOX_FILE, 'r') as bbox_file:
    img_lines = list_file.read().splitlines()
    bbox_lines = bbox_file.read().splitlines()
    n = int(img_lines[0])
    for i in range(n):
        img_line = img_lines[i + 2]
        img_line = re.sub(' +', ' ', img_line)
        img_path, category_id = img_line.split(' ')
        # it's possible, because an order in both files is the same
        bbox_line = bbox_lines[i + 2]
        bbox_line = re.sub(' +', ' ', bbox_line)
        _, x1, y1, x2, y2 = bbox_line.split(' ')
        with Image.open(INPUT_DIR + img_path) as im:
            w, h = im.size

        name = categories[int(category_id)]

        path = os.path.join(*(img_path.split(os.path.sep)[1:]))
        anno_path = OUTPUT_DIR + os.path.splitext(path)[0] + ".xml"

        if not os.path.exists(os.path.dirname(anno_path)):
            os.makedirs(os.path.dirname(anno_path))

        with open(anno_path, 'w') as output_file:
            output_file.write(TEMPLATE.format(w, h, name, int(x1), int(y1), int(x2), int(y2)))

        if i % 1000 == 0:
            print("Processed {0}/{1}".format(i, n))
