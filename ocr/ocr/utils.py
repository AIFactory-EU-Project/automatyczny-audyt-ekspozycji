import json
import logging
import os
import cv2

from glob import iglob
from enum import Enum
from ocr.config.auto import config
from vision.helpers import file_helpers


TAGS_DIR_NAME = "tags"


class Mode(Enum):
    __order__ = 'DATE SERIAL_NUMBER AVAILABLE_AREA'
    DATE = 0
    SERIAL_NUMBER = 1
    AVAILABLE_AREA = 2


def load_file_paths(input_dir):
    file_paths = []
    input_dir = os.path.join(input_dir, '*')
    for path in iglob(input_dir):
        front_dir = os.path.join(path, config.aug.front_dir)
        if 'empty' in front_dir:
            continue
        if os.path.exists(front_dir):
            for image_name in os.listdir(front_dir):
                front_path = os.path.join(path, front_dir, image_name)
                tag_path = front_path.replace(config.aug.front_dir, TAGS_DIR_NAME).replace(config.aug.img_file_format, 'json')

                if file_helpers.if_exists(front_path) and file_helpers.if_exists(tag_path):
                    file_paths.append(front_path.split('.')[0])
        else:
            logging.warning('"{}" not found'.format(front_dir))

    return file_paths


def load_labels(input_dir):
    labels = {}
    input_dir = os.path.join(input_dir, '*')
    for path in iglob(input_dir):
        tag_dir = os.path.join(path, TAGS_DIR_NAME)
        for tag_file_name in os.listdir(tag_dir):
            tag_path = os.path.join(tag_dir, tag_file_name)
            front_path = tag_path.replace(TAGS_DIR_NAME, config.aug.front_dir).replace('json', config.aug.img_file_format)

            with open(tag_path, 'r') as fp:
                labels[front_path.split('.')[0]] = json.load(fp)

    return labels


def get_label_if_exists(labels, image_id, label_name):
    try:
        label = labels[image_id][label_name]
    except KeyError:
        label = None

    if not label:
        logging.warning('"{}": {} label not found.'.format(image_id, label_name))
        return None

    return label


def tag_validation(name, labels):
    """ Check if .json file contains correct tags """
    label = labels[name]
    if len(label[Mode.AVAILABLE_AREA.name]) == 0 \
            or len(label[Mode.DATE.name]) != 1 \
            or len(label[Mode.SERIAL_NUMBER.name]) != 1:
        logging.error('"{}" invalid .json file'.format(name))
        return False
    return True


def convert_positions(shape, labels):
    for rect in labels:
        for point in rect:
            point[0] = int(point[0] * shape[1])
            point[1] = int(point[1] * shape[0])

    return labels


def show(title, img):
    cv2.imshow(title, img)
    cv2.waitKey()
