""" Apply perspective transformations. """

import random
import cv2
import numpy as np

from vision.aug.transformations.transformation import Transformation
from vision.aug import utils as aug_utils


class PerspectiveTransformation(Transformation):
    @staticmethod
    def transform_perspective_and_get_matrix(img, max_warp=0.1, mtx=None):
        """
            Find four random points within image and apply perspective transformation
        Args:
            img: input image
            max_warp: limiter of points positions
            mtx: perspective matrix
        """
        im_height, im_width = img.shape[:2]

        if mtx is None:
            b = int(min(im_height, im_width) * max_warp)
            r = random.randint

            pts2 = np.float32([[0, 0], [im_width-1, 0], [0, im_height-1], [im_width-1, im_height-1]])

            pts1 = np.float32([[r(0, b), r(0, b)],
                               [im_width - 1 - r(0, b), r(0, b)],
                               [r(0, b), im_height - 1 - r(0, b)],
                               [im_width - 1 - r(0, b), im_height - 1 - r(0, b)]])

            mtx = cv2.getPerspectiveTransform(pts1, pts2)

        return cv2.warpPerspective(img, mtx, (im_width, im_height)), mtx

    @staticmethod
    def transform_perspective(img, max_warp=0.1, mtx=None):
        image, _ = PerspectiveTransformation.transform_perspective_and_get_matrix(img, max_warp, mtx)
        return image

    @staticmethod
    def perspective_transformation(image, ratio=.1, fill_border=False, squeeze=False, image_only=False):
        height, width = image.shape[:2]

        pts1 = np.float32([[0, height - 1], [width - 1, height - 1], [width - 1, 0], [0, 0]])
        pts2 = np.float32([[0, height - 1], [width - 1, height - 1], [width - 1, 0], [0, 0]])

        idxs = [-4, -2] if squeeze else [-4, -3, -2, -1]
        idx = random.choice(idxs)

        if squeeze :
            dist = height * ratio

            # translate y-coordinate
            pts2[idx][1] += dist
            pts2[idx + 3][1] += dist

            h_dist = int(abs(dist))
            height += h_dist

            # "squeeze" box
            squeeze_dist = width * ratio / 2
            pts2[1][0] -= squeeze_dist
            pts2[2][0] -= squeeze_dist
        else:
            dist = aug_utils.distance_between(pts2[idx], pts2[idx + 3]) * ratio

            dist = dist if idx in [-4, -3] else -dist
            # check whether to translate x- or y-coordinate
            i = 0 if idx % 2 else 1
            pts2[idx][i] -= dist
            pts2[idx + 3][i] += dist

        mtx = cv2.getPerspectiveTransform(pts1, pts2)
        fill_border = bool(random.getrandbits(1)) if fill_border in ('None',None) else fill_border
        if fill_border:
            warped = cv2.warpPerspective(image, mtx, (width, height), borderMode=cv2.BORDER_REPLICATE)
        else:
            warped = cv2.warpPerspective(image, mtx, (width, height), borderValue=(127, 127, 127))

        # trim image
        x, y, box_w, box_h = cv2.boundingRect(pts2)
        x = max(0, x)
        y = max(0, y)
        perspective_image = warped[y:y + box_h, x:x + box_w]

        if image_only:
            return perspective_image

        return perspective_image, mtx

    @staticmethod
    def squeeze_perspective_transformation(image, ratio=.1, fill_border=False, image_only=False):
        return PerspectiveTransformation.perspective_transformation(image, ratio=ratio, fill_border=fill_border, squeeze=True, image_only=image_only)
