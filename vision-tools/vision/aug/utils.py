import math
import random
import numpy as np


def weighted_choice(choices_dict, probability_sum=None):
    if probability_sum is None:
        probability_sum = sum(v for k, v in choices_dict.items())

    r = random.uniform(0, probability_sum)
    upto = 0
    for k, v in choices_dict.items():
        if upto + v >= r:
            return k
        upto += v
    return ""


def order_points(points):
    """ Return ordered points. Do not use with stock - generate wrong order! """
    if points is not np.ndarray:
        points = np.array(points, dtype=np.int32)

    x = points[:, 0]
    y = points[:, 1]
    cx = np.mean(x)
    cy = np.mean(y)
    angles = np.arctan2(y - cy, x - cx)
    ordered = points[angles.argsort(), :]

    return np.array(ordered, dtype=np.int)


def find_point_between(p1, p2, ratio):
    """ Return point between two others (with given distance) """
    inv_ratio = 1 - ratio
    return ratio*p1[0] + inv_ratio*p2[0], ratio*p1[1] + inv_ratio*p2[1]


def distance_between(p1, p2):
    """ Return distance between two points """
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
