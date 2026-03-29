""" Apply affine transformation """

import random
import cv2
import numpy as np

from vision.aug.transformations.transformation import Transformation


class AffineTransformation(Transformation):
    @staticmethod
    def rotate_bound(image, angle, interpolation=cv2.INTER_LINEAR, mode=cv2.BORDER_CONSTANT, value=(255, 255, 255), change_size=True):
        """ Rotate and resize image """
        im_height, im_width = image.shape[:2]
        if change_size:
            center_x, center_y = im_width // 2, im_height // 2

            matrix = cv2.getRotationMatrix2D((center_x, center_y), angle, 1.0)
            cos = np.abs(matrix[0, 0])
            sin = np.abs(matrix[0, 1])

            new_width = int((im_height * sin) + (im_width * cos))
            new_height = int((im_height * cos) + (im_width * sin))

            # Adjust rotation matrix to take translation into account
            matrix[0, 2] += (new_width / 2) - center_x
            matrix[1, 2] += (new_height / 2) - center_y

            return cv2.warpAffine(image, matrix, (new_width, new_height),
                                  flags=interpolation, borderMode=mode,
                                  borderValue=value), matrix, new_width, new_height

        matrix = cv2.getRotationMatrix2D((im_width / 2, im_height / 2), angle, 1.0)

        img = cv2.warpAffine(image, matrix, (im_width, im_height), flags=interpolation, borderMode=mode, borderValue=value)

        return img, matrix, im_height/2, im_width/2

    @staticmethod
    def rotation(image, angle=0, border_value=None):
        im_height, im_width = image.shape[:2]

        if border_value is not None:
            image, _, _, _ = AffineTransformation.rotate_bound(image, angle, value=border_value)
        else:
            image, _, _, _ = AffineTransformation.rotate_bound(image, angle, value=image[0][0][:].astype(int))

        return cv2.resize(image, (im_width, im_height), interpolation=cv2.INTER_CUBIC)

    @staticmethod
    def stretch(image, x_scale=0, y_scale=0):
        im_height, im_width = image.shape[:2]

        if random.getrandbits(1):
            new_w = (1 - x_scale) * im_width
            new_w, new_h = int(new_w), im_height
        else:
            new_h = (1 - y_scale) * im_height
            new_w, new_h = im_width, int(new_h)

        return cv2.resize(image, (new_w, new_h))

    @staticmethod
    def rotate(image, angle=None, border=(127, 127, 127), image_only=False):
        if angle is None:
            angle = random.choice([0, 90, 180, 270])

        if image_only:
            return AffineTransformation.rotate_bound(image, angle, value=border)[0]

        return AffineTransformation.rotate_bound(image, angle, value=border)[:2]

    @staticmethod
    def resize(image, width=None, height=None, magnitude=.1, interpolation=cv2.INTER_AREA, image_only=False):
        img_height, img_width = image.shape[:2]
        if not width or not height:
            height = int(img_height * magnitude)
            width = int(img_width * magnitude)
            resized = cv2.resize(image, dsize=(width, height), interpolation=interpolation)
            if not image_only:
                return resized, width, height
        else:
            resized = cv2.resize(image, dsize=(width, height), interpolation=interpolation)

        return resized

    @staticmethod
    def flip(image, vertical=True, horizontal=False):
        if not vertical and not horizontal:
            return image
        if vertical and horizontal:
            return cv2.flip(image, -1)
        if vertical:
            return cv2.flip(image, 1)

        return cv2.flip(image, 0)
