"""
    Add random contours to input image:
        - random shape contours
        - round shape contours
        - templates loaded from file
"""
from __future__ import print_function
import random
import cv2
from enum import Enum

from vision.aug.transformations.transformation import Transformation

ITERATIONS_LIMITER = 1000


class Direction(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


class ContoursAdderTransformation(Transformation):
    @staticmethod
    def get_cut_letter_coords(dir_id, border, shape, b_range):
        border = int(border * random.uniform(*b_range))

        if dir_id.name == Direction.TOP.name:
            return [(0, 0), (0, border), (shape[1]-1, border), (shape[1]-1, 0)]
        elif dir_id.name == Direction.BOTTOM.name:
            return [(0, shape[0]-1-border), (shape[1]-1, shape[0]-1-border), (shape[1]-1, shape[0]-1), (0, shape[0]-1)]
        elif dir_id.name == Direction.LEFT.name:
            return [(0, 0), (border, 0), (border, shape[0]-1), (0, shape[0]-1)]
        elif dir_id.name == Direction.RIGHT.name:
            return [(shape[1]-1-border, 0), (shape[1]-1, 0), (shape[1]-1, shape[0]-1), (shape[1]-1-border, shape[0]-1)]

    @staticmethod
    def fit_image_to_available_area(cut_text, dir_id, coordinates):
        height = abs(coordinates[0][1] - coordinates[2][1])
        width = abs(coordinates[0][0] - coordinates[2][0])

        if dir_id.name == Direction.TOP.name:
            return cut_text[cut_text.shape[0]-1-height:cut_text.shape[0]-1, 0:width]

        elif dir_id.name == Direction.BOTTOM.name:
            return cut_text[0:height, 0:width]

        elif dir_id.name == Direction.LEFT.name:
            return cut_text[0:height, cut_text.shape[1]-1-width:cut_text.shape[1]-1]

        elif dir_id.name == Direction.RIGHT.name:
            return cut_text[0:height, 0:width]

    @staticmethod
    def get_random_offsets(direction, coords, crop):
        x_offset = 0
        y_offset = 0

        if direction.name == Direction.TOP.name or direction.name == Direction.BOTTOM.name:
            x_diff = int(abs(coords[0][0] - coords[3][0])) - crop.shape[1]
            if x_diff > 0:
                x_offset = random.randint(0, x_diff)

        if direction.name == Direction.LEFT.name or direction.name == Direction.RIGHT.name:
            y_diff = int(abs(coords[0][1] - coords[3][1])) - crop.shape[0]
            if y_diff > 0:
                y_offset = random.randint(0, y_diff)

        return x_offset, y_offset

    @staticmethod
    def add_template_contour(image, contour, direction=None, contour_width=(.6, .9), margin=None):
        """ Load contour from image file and insert in a random position """
        h = int(random.uniform(.8, 2) * image.shape[0])
        w = int(contour.shape[1] / (contour.shape[0] / float(h)))
        symbol = cv2.resize(contour, (w, h), interpolation=cv2.INTER_CUBIC)

        if margin is None:
            margin = int(2 * image.shape[0])

        if direction is None:
            direction = Direction(random.choice([2, 3]))

        image = cv2.copyMakeBorder(image, 0, 0, margin, margin, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255, 0))
        coords = ContoursAdderTransformation.get_cut_letter_coords(direction, margin, image.shape, contour_width)
        symbol = ContoursAdderTransformation.fit_image_to_available_area(symbol, direction, coords)

        x_offset, y_offset = ContoursAdderTransformation.get_random_offsets(direction, coords, symbol)

        print(image.shape)
        print(symbol.shape)

        image[y_offset + coords[0][1]:y_offset + coords[0][1] + symbol.shape[0],
              x_offset + coords[0][0]:x_offset + coords[0][0] + symbol.shape[1]] = symbol

        return Transformation.fit_borders(image)

    @staticmethod
    def draw_points(image, last, color, limit):
        last_x, last_y = last
        for _ in range(limit):
            image[last_y, last_x, :] = color

            for _ in range(ITERATIONS_LIMITER):
                x, y = random.choice([(last_x - 1, last_y), (last_x, last_y - 1), (last_x + 1, last_y), (last_x, last_y + 1)])
                if 0 < x < image.shape[1] and 0 < y < image.shape[0]:
                    last_x, last_y = x, y
                    break

    @staticmethod
    def draw_random_contour(image, color=None, limit=500, iterations=1):
        """ Draw random curves """
        if color is None:
            color = [255, 255, 255]

        for _ in range(iterations):
            x, y = random.randint(0, image.shape[1] - 1), random.randint(0, image.shape[0] - 1)
            ContoursAdderTransformation.draw_points(image, (x, y), color, limit)

        return image

    @staticmethod
    def random_dirt(image, max_radius=5):
        """ Draw random radial contour """
        repeated_dirt_probability = 0.5
        while True:
            if random.random() < repeated_dirt_probability:
                return image

            center = (random.randint(0, image.shape[1] - 1), random.randint(0, image.shape[0] - 1))
            cv2.circle(image, center, random.randint(0, max_radius), Transformation.random_dark_color(), cv2.FILLED)

