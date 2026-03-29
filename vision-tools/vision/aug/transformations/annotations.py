from __future__ import print_function
import cv2
import random
import numpy as np

from vision.aug.transformations.perspective import PerspectiveTransformation


class AnnotationsTransformation:
    @staticmethod
    def transform_perspective(image, points_sets, max_warp=(0, .2)):
        image, mtx = AnnotationsTransformation.transform_perspective_get_matrix(image, max_warp)
        for key, points in points_sets.items():
            try:
                points = AnnotationsTransformation.transform_points(points, mtx)
            except:
                print(key, points)

            points_sets[key] = points

        return image, points_sets

    @staticmethod
    def transform_perspective_get_matrix(image, max_warp):
        image, mtx = PerspectiveTransformation().transform_perspective_and_get_matrix(
            image, max_warp=random.uniform(*max_warp))
        return image, mtx


    @staticmethod
    def transform_points(points, mtx):
        points = np.array(points, dtype='float32')
        points = np.array([points])
        points = cv2.perspectiveTransform(points, mtx)
        points = points[0].astype(int).tolist()
        return points

    @staticmethod
    def rotate(image, points_sets, angle, mode=cv2.BORDER_CONSTANT, value=(255, 255, 255, 0)):
        img, mtx = AnnotationsTransformation.rotate_get_matrix(image, angle, mode, value)

        output_points = {}
        for key, points in points_sets.items():
            output_points[key] = []
            for point in points:
                point = np.array([point[0], point[1], 1])
                rotated = np.dot(mtx, point.T).astype(int).tolist()
                output_points[key].append(rotated)
        return img, output_points

    @staticmethod
    def rotate_get_matrix(image, angle, mode=cv2.BORDER_CONSTANT, value=(255, 255, 255, 0), center=None, add_bound=True):
        (h, w) = image.shape[:2]
        if center is None:
            center_x, center_y = (w / 2, h / 2)
        else:
            center_x, center_y = center

        mtx = cv2.getRotationMatrix2D((center_x, center_y), angle, 1.0)
        if add_bound:
            cos = np.abs(mtx[0, 0])
            sin = np.abs(mtx[0, 1])
            new_width = int((h * sin) + (w * cos))
            new_height = int((h * cos) + (w * sin))
            mtx[0, 2] += (new_width / 2) - center_x
            mtx[1, 2] += (new_height / 2) - center_y
        else:
            new_width = w
            new_height = h

        img = cv2.warpAffine(image, mtx, (new_width, new_height),
                             flags=cv2.INTER_CUBIC, borderMode=mode, borderValue=value)
        return img, mtx

    @staticmethod
    def resize(image, points, diff=(0, 2.)):
        # TODO

        return image, points
