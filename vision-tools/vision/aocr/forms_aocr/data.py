import cv2
import logging
import os


def form_samples(path="", paths_only=False):
    if not path or not os.path.exists(path):
        logging.error("Empty path!")
        raise Exception("Empty path! Cannot create datasets.")

    with open(path) as f:
        lines = f.read().splitlines()

    for line in lines:
        img, label = line.split(' ', 1)
        if paths_only:
            yield img, label
        else:
            yield cv2.imread(img), label
