""" Common tools for aug package. """
import cv2

from ocr.aug.config import config


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def flip_image(img, number_of_flips):
    for i in range(number_of_flips):
        img = cv2.transpose(img)
        img = cv2.flip(img, flipCode=1)

    return img


def apply_scale(size, extra=0):
    return int(size[0] * (config.params.inserted_text_scale + extra)), \
           int(size[1] * (config.params.inserted_text_scale + extra))


def is_horizontally_oriented(shape=None):
    if shape is not None:
        return shape[1] > shape[0]


def is_vertically_oriented(shape=None):
    if shape is not None:
        return shape[0] > shape[1]
