""" Finding positions for generated date and serial number crops. """
import logging
import random
import cv2
import numpy as np

from ocr.aug import aug_utils
from ocr.aug.config import config
from vision.aug.transformations.perspective import PerspectiveTransformation


class PositionFinder:
    def get_two_related_random_positions(self, img, coords, shape1, shape2):
        if aug_utils.is_vertically_oriented(shape1):
            probability = config.params.horizontal_orientation
        else:
            probability = config.params.vertical_orientation

        if random.random() < probability:
            return self.get_two_vertically_related_positions(img, coords, shape1, shape2)
        else:
            return self.get_two_horizontally_related_positions(img, coords, shape1, shape2)

    @staticmethod
    def get_two_horizontally_related_positions(img, coords, crop1_shape, crop2_shape):
        if aug_utils.is_vertically_oriented(crop1_shape):
            max_break = config.params.max_vertical_break
            min_break = config.params.min_vertical_break
        else:
            max_break = config.params.max_horizontal_break
            min_break = config.params.min_horizontal_break

        random_break = max(int(max_break * random.random()**2), min_break)
        joined_shape = max(crop1_shape[0], crop2_shape[0]), crop1_shape[1] + crop2_shape[1] + random_break

        img, point1 = PositionFinder().get_random_position(img, coords, joined_shape)
        point2 = None

        if point1 is not None:
            point2 = (point1[0] + crop1_shape[1] + random_break, point1[1])

        return img, point1, point2

    @staticmethod
    def get_two_vertically_related_positions(img, coords, crop1_shape, crop2_shape):
        if aug_utils.is_vertically_oriented(crop1_shape):
            max_break = config.params.max_horizontal_break
            min_break = config.params.min_horizontal_break
        else:
            max_break = config.params.max_vertical_break
            min_break = config.params.min_vertical_break

        shapes = [crop1_shape, crop2_shape]
        max_width_index = 0 if shapes[0][1] > shapes[1][1] else 1

        random_break = max(int(max_break * random.random()**2), min_break)
        joined_shape = random_break + crop1_shape[0] + crop2_shape[0], max(crop1_shape[1], crop2_shape[1])

        img, point1 = PositionFinder().get_random_position(img, coords, joined_shape)

        if point1 is not None:
            point1 = list(point1)
            points = [point1, None]

            points[1] = [points[0][0], points[0][1] + int(crop1_shape[0] + random_break)]

            if random.random() < config.params.align_right:
                points[1 - max_width_index][0] += shapes[max_width_index][1] - shapes[1 - max_width_index][1]

            elif random.random() < config.params.align_random:
                points[1 - max_width_index][0] += random.randint(0, shapes[max_width_index][1] - shapes[1 - max_width_index][1])

            return img, points[0], points[1]

        return img, None, None

    def get_two_unrelated_random_positions(self, img, coords, crop1_shape, crop2_shape):
        point1 = None
        point2 = None
        mask = self.coords_to_binary_map(coords, map_img=np.zeros(img.shape[:2], dtype=np.uint8))

        img, mask = self.apply_random_flip(img, mask)
        img, mask = self.transform_perspective(img, mask)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if isinstance(contours, list):
            contours = contours[0]

        border_x, border_y, w, h = cv2.boundingRect(contours)
        mask = mask[border_y:border_y + h, border_x:border_x + w]

        p1 = self.random_rect_in_contour(mask, crop1_shape)
        if p1 is not None:
            point1 = (border_x + p1[0], border_y + p1[1])
            cv2.rectangle(mask, p1, (p1[0] + crop1_shape[1], p1[1] + crop1_shape[0]), 0, cv2.FILLED)

        p2 = self.random_rect_in_contour(mask, crop2_shape)
        if p2 is not None:
            point2 = (border_x + p2[0], border_y + p2[1])
            cv2.rectangle(mask, p2, (p2[0] + crop2_shape[1], p2[1] + crop2_shape[0]), 0, cv2.FILLED)

        return img, point1, point2

    @staticmethod
    def apply_random_flip(image, mask):
        if config.params.random_bg_flip > random.random():
            threshold_ratio = 1.75
            if image.shape[1]/float((image.shape[0])) < threshold_ratio:
                num_of_flips = random.randint(0, 3)     # 0, 90, 180 or 270 degrees
                mask = aug_utils.flip_image(mask, num_of_flips)
                image = aug_utils.flip_image(image, num_of_flips)
            else:
                num_of_flips = random.choice([0, 2])    # 0 or 180 degrees
                mask = aug_utils.flip_image(mask, num_of_flips)
                image = aug_utils.flip_image(image, num_of_flips)

        return image, mask

    def get_random_position(self, img, coords, crop_shape, flip=True):
        p = None
        mask = self.coords_to_binary_map(coords, map_img=np.zeros(img.shape[:2], dtype=np.uint8))

        if flip:
            img, mask = self.apply_random_flip(img, mask)

        img, mask = self.transform_perspective(img, mask)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not len(contours):
            return img, p

        contours = contours[0]
        border_x, border_y, w, h = cv2.boundingRect(contours)
        mask = mask[border_y:border_y + h, border_x:border_x + w]

        p_random = self.random_rect_in_contour(mask, crop_shape)
        if p_random is not None:
            p = border_x + p_random[0], border_y + p_random[1]

        return img, p

    def get_widest_crop(self, img, coords, height):
        mask = self.coords_to_binary_map(
            coords, map_img=np.zeros(img.shape[:2], dtype=np.uint8))

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if isinstance(contours, list):
            contours = contours[0]

        border_x, border_y, w, h = cv2.boundingRect(contours)
        mask = mask[border_y:border_y + h, border_x:border_x + w]
        img = img[border_y:border_y + h, border_x:border_x + w]

        return self.random_widest_crop_in_contour(mask, img, height)

    @staticmethod
    def coords_to_binary_map(coords, map_img):
        for coord in coords:
            p1, p2 = coord
            point1 = min(p1[0], p2[0]), min(p1[1], p2[1])
            point2 = max(p1[0], p2[0]), max(p1[1], p2[1])
            cv2.rectangle(map_img, point1, point2, 255, cv2.FILLED)

        return map_img

    @staticmethod
    def random_rect_in_contour(drawing, crop_shape, limiter=config.params.iterations_limiter):
        for i in range(limiter):
            p_x = random.randint(0, drawing.shape[1] - 1)
            p_y = random.randint(0, drawing.shape[0] - 1)

            try:
                rect_sum = np.sum(drawing[p_y:p_y + crop_shape[0], p_x:p_x + crop_shape[1]])
            except IndexError:
                continue

            if rect_sum != crop_shape[0] * crop_shape[1] * 255:
                continue

            return p_x, p_y

        return None

    @staticmethod
    def get_widest_area(drawing, x, y, height):
        step = 5
        left = step
        right = step

        while np.sum(drawing[y:y+height, x-left:x]) == left*height*255:
            left += step
        left -= step

        while np.sum(drawing[y:y+height, x:x + right]) == right*height*255:
            right += step
        right -= step

        return (left+right)*height, (x - left, x + right, y, y + height)

    @staticmethod
    def random_widest_crop_in_contour(drawing, image, height):
        max_area = 0
        best_coords = None

        for i in range(config.params.max_widest_crop_iterations):
            p_x = random.randint(0, drawing.shape[1] - 1)
            p_y = random.randint(0, drawing.shape[0] - 1)

            try:
                area, coords = PositionFinder.get_widest_area(drawing, p_x, p_y, height)
                if area > max_area:
                    max_area = area
                    best_coords = coords

            except IndexError:
                continue

        if best_coords is None:
            logging.warning('{} iterations was not enough to find the widest crop position'.format(config.params.max_widest_crop_iterations))
            return None

        left, right, top, bottom = best_coords
        return image[top:bottom, left:right]

    @staticmethod
    def transform_perspective(image1, image2):
        image1, mtx = PerspectiveTransformation().transform_perspective_and_get_matrix(image1, max_warp=random.uniform(0., 0.20))
        image2, mtx = PerspectiveTransformation().transform_perspective_and_get_matrix(image2, mtx=mtx)

        return image1, image2
