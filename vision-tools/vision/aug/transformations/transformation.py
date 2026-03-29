""" Common tools for transformation classes """

import numpy as np
import cv2
import random
import logging


class Transformation(object):
    @staticmethod
    def hsv_to_rgb(hsv):
        color = cv2.cvtColor(cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2RGB)[0][0]

        return np.array([int(color[0]), int(color[1]), int(color[2])])

    @staticmethod
    def random_bright_color():
        hsv = np.array([[[random.randint(0, 360),
                          random.randint(0, 50),
                          random.randint(100, 255)]]], dtype=np.uint8)

        return Transformation.hsv_to_rgb(hsv)

    @staticmethod
    def random_dark_color():
        hsv = np.array([[[random.randint(0, 360),
                          random.randint(0, 200),
                          random.randint(30, 120)]]], dtype=np.uint8)

        return Transformation.hsv_to_rgb(hsv)

    @staticmethod
    def fit_borders(image, horizontal_only=False, vertical_only=False):
        assert not (vertical_only and horizontal_only)
        try:
            tmp = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
            tmp = 255 - tmp

            oy_sum = np.sum(tmp, axis=1)
            oy_not_zeros = np.where(oy_sum != 0)[0]

            ox_sum = np.sum(tmp, axis=0)
            ox_not_zeros = np.where(ox_sum != 0)[0]

            # display margins
            # tmp[oy_not_zeros[0], :] = 255
            # tmp[oy_not_zeros[-1], :] = 255
            # tmp[:, ox_not_zeros[0]] = 255
            # tmp[:, ox_not_zeros[-1]] = 255

            b = 2
            if not horizontal_only:
                image = image[max(oy_not_zeros[0] - b, 0):min(oy_not_zeros[-1] + b, image.shape[0] - 1), :]

            if not vertical_only:
                image = image[:, max(ox_not_zeros[0] - b, 0):min(ox_not_zeros[-1] + b, image.shape[1] - 1)]

        except IndexError:
            logging.error('fit_borders(): Content not found.')

        return image

    @staticmethod
    def get_random_rect_size(area, thresh_h, thresh_w):
        """ Find random rectangle's sides """
        crop_height = random.randint(int(area / thresh_w), thresh_h)
        crop_width = int(area / crop_height)

        return min(crop_height, thresh_h), min(crop_width, thresh_w)

    @staticmethod
    def get_crop_shape(height, width, ratio, factor=1.):
        """ Return height and width of crop """
        crop_area = ratio * height * width
        thresh_h, thresh_w = int(factor * height), int(factor * width)
        if width > height:
            crop_height, crop_width = Transformation.get_random_rect_size(crop_area, thresh_h, thresh_w)
        else:
            crop_width, crop_height = Transformation.get_random_rect_size(crop_area, thresh_w, thresh_h)

        return crop_height, crop_width

    @staticmethod
    def find_random_corner_rect(height, width, ratio):
        """ Find random rectangle around image corner """
        crop_height, crop_width = Transformation.get_crop_shape(height, width, ratio, factor=.75)
        corners = [(0, 0), (0, height - 1), (width - 1, height - 1), (width - 1, 0)]
        c = random.choice(corners)
        crop_y = abs(c[1] - crop_height)
        crop_x = abs(c[0] - crop_width)
        y_min, y_max = (c[1], crop_y) if c[1] < crop_y else (crop_y, c[1])
        x_min, x_max = (c[0], crop_x) if c[0] < crop_x else (crop_x, c[0])
        return y_min, y_max, x_min, x_max

    @staticmethod
    def find_random_rect(ratio, height, width, corner=False):
        """ Find random rectangle within image """
        if corner:
            return Transformation.find_random_corner_rect(height, width, ratio)

        crop_height, crop_width = Transformation.get_crop_shape(height, width, ratio)

        width_only = False
        height_only = False
        x = 0
        y = 0

        if crop_height == height:
            width_only = True

        if crop_width == width:
            height_only = True

        # do not include last column
        width -= 1
        height -= 1
        crop_width -= 1
        crop_height -= 1

        while True:
            if not height_only:
                x = random.randint(0, width)
            if not width_only:
                y = random.randint(0, height)
            if x + crop_width <= width and y + crop_height <= height:
                return y, y + crop_height, x, x + crop_width
            if x - crop_width >= 0 and y - crop_height >= 0:
                return y - crop_height, y, x - crop_width, x
            if x + crop_width <= width and y - crop_height >= 0:
                return y - crop_height, y, x, x + crop_width
            if x - crop_width >= 0 and y + crop_height <= height:
                return y, y + crop_height, x - crop_width, x
