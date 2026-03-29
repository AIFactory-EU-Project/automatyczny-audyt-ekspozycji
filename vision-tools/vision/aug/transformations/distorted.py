""" Apply distortions i.e.:
    - move letters separately
    - pixelize font
    - make font noisy
    - cut vertically/horizontally
"""

import random
import cv2
import numpy as np

from vision.aug.transformations.transformation import Transformation


class DistortedTransformation(Transformation):
    @staticmethod
    def erode(image, kernel_size=5, reversed=False):
        kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        er, dil = cv2.erode, cv2.dilate
        if reversed:
            er, dil = dil, er

        image[:, :, 0] = er(image[:, :, 0], kernel, iterations=1)
        image[:, :, 1] = er(image[:, :, 1], kernel, iterations=1)
        image[:, :, 2] = er(image[:, :, 2], kernel, iterations=1)
        if image.shape[2] > 3:
            image[:, :, 3] = dil(image[:, :, 3], kernel, iterations=1)

        return image

    @staticmethod
    def dilate(image, kernel_size=3):
        return DistortedTransformation.erode(image, kernel_size, reversed=True)

    @staticmethod
    def erode_text(image):
        # TODO
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        image = 255 - image
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)

        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGBA)

        return image

    @staticmethod
    def get_letters_bounding_boxes(in_image):
        last_empty = None
        last_letter = None
        top_border = None
        bottom_border = None
        borders = []

        image = in_image.copy()
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)

        im_height, im_width = image.shape[:2]

        # Find top/bottom border
        for i in range(im_height):
            column_sum = sum(image[i, :])
            if column_sum != 255 * im_width and top_border is None:
                top_border = i

            column_sum = sum(image[-i, :])
            if column_sum != 255 * im_width and bottom_border is None:
                bottom_border = im_height - i

            if top_border is not None and bottom_border is not None:
                break

        # Find vertical borders
        for i in range(im_width):
            column_sum = sum(image[:, i])
            if column_sum != 255 * im_height:
                if last_letter != i - 1:
                    borders.append(i)
                last_letter = i
            else:
                if last_empty is not None and last_empty != i - 1:
                    borders.append(i)
                last_empty = i

        vertical_borders = sorted(borders)
        crop_borders = []

        for i in range(len(vertical_borders), 2):
            crop_borders.append([top_border, bottom_border, vertical_borders[i], vertical_borders[i + 1]])

        return crop_borders

    @staticmethod
    def erode_letters_separately(image):
        # TODO
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        image = cv2.copyMakeBorder(image, 1, 1, 1, 1, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255, 255))

        borders = DistortedTransformation.get_letters_bounding_boxes(image)
        image = 255 - image

        for b in borders:
            y1, y2, x1, x2 = b
            single_letter = image[y1:y2, x1:x2]
            single_letter = cv2.erode(single_letter, kernel, iterations=random.randint(0, 4))
            image[y1:y2, x1:x2] = single_letter

        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGBA)
        image[:, :, 3] = 255
        image = 255 - image

        return image

    @staticmethod
    def move_letters_separately(image, max_dev_ox=0.02, max_dev_oy=0.15):
        im_height, im_width = image.shape[:2]
        fill_color = (255, 255, 255, 0)

        h = int(max_dev_oy * im_height + 1)
        w = int(max_dev_ox * im_width + 1)
        image = cv2.copyMakeBorder(image, h, h, w, w, cv2.BORDER_CONSTANT, value=fill_color)
        borders = DistortedTransformation.get_letters_bounding_boxes(image)

        for b in borders:
            y1, y2, x1, x2 = b
            ox_dev = int(random.uniform(-max_dev_ox, max_dev_ox) * im_width) / 2
            oy_dev = int(random.uniform(-max_dev_oy, max_dev_oy) * im_height) / 2

            tmp_x1, tmp_x2 = x1 + ox_dev, x2 + ox_dev
            tmp_y1, tmp_y2 = y1 + oy_dev, y2 + oy_dev

            tmp_tensor = image[y1:y2, x1:x2].copy()
            image[max(0, y1 - 1):min(image.shape[0], y2 + 1), max(0, x1 - 1):min(image.shape[1], x2 + 1)] = fill_color
            image[tmp_y1:tmp_y2, tmp_x1:tmp_x2] = tmp_tensor

        return cv2.resize(image, (im_width, im_height), interpolation=cv2.INTER_CUBIC)

    @staticmethod
    def get_edge_points(shape):
        points = []
        if random.getrandbits(1):
            # horizontal
            points.extend([(0, shape[0]-1), (shape[1]-1, shape[0]-1)])
            height = random.randint(0, shape[0]-1)
            points.append((shape[1]-1, height))
            points.append((0, height))
        else:
            # vertical
            points.extend([(0, 0), (0, shape[0]-1)])
            width = random.randint(0, shape[1]-1)
            points.append((width, shape[0]-1))
            points.append((width, 0))

        return np.array([points])

    @staticmethod
    def random_edge(image):
        points = DistortedTransformation.get_edge_points(image.shape)
        bg_color = Transformation.random_bright_color()
        cv2.fillPoly(image, points, bg_color)

        return image

    @staticmethod
    def pixelize_dark(image, pixel_size=2, color=None):
        if color is None:
            color = [0, 0, 0, 255]

        image = 255 - image
        ox_number = image.shape[1] / pixel_size
        oy_number = image.shape[0] / pixel_size

        image2 = np.zeros(image.shape, dtype=np.uint8)
        image2[:, :, :3] = 255

        for i in range(ox_number):
            for j in range(oy_number):
                h = j * pixel_size
                w = i * pixel_size

                if np.sum(image[h:h+pixel_size, w:w+pixel_size, :3]) != 0:
                    image2[h:h+pixel_size, w:w+pixel_size, :4] = color

        b = 3
        Transformation.copy_make_border(image2, top=b, bottom=b, left=b, right=b)

        return image2

    @staticmethod
    def noise(mask, image, color_diff=10, percent=0.05, radius=10):
        im_height, im_width = image.shape[:2]
        tmp = image.copy()
        tmp = 255 - tmp
        tmp = cv2.cvtColor(tmp, cv2.COLOR_RGBA2GRAY)
        _, tmp = cv2.threshold(tmp, 1, 255, cv2.THRESH_BINARY)

        number = int(percent * im_height * im_width)
        for _ in range(number):
            c = random.randint(0, color_diff)
            color = [c, c, c, 255]

            oy = random.randint(0, im_height - 1)
            ox = random.randint(0, im_width - 1)
            if mask[oy, ox]:
                cv2.circle(image, (ox, oy), 0, color, radius)

        return image

    @staticmethod
    def apply_noises(img, configs):
        mask = img.copy()
        mask = cv2.cvtColor(mask, cv2.COLOR_RGBA2GRAY)
        mask = 255 - mask

        img2 = np.zeros(img.shape, dtype=np.uint8)
        img2[:, :, :3] = 255

        config = random.choice(configs)
        for params in config:
            img2 = DistortedTransformation.noise(mask, img2, *params)

        return img2

    @staticmethod
    def apply_noises_dotted_font(img):
        """ Apply different kinds of noises defined in configs (dotted fonts)
            Single config row:
                [x, y, z]
            x - max deviation from base color
            y - density of noise in percent
            z - radius of single dot
        """
        configs = [
            [
                [20, 2.2, 1],
            ]
        ]

        return DistortedTransformation.apply_noises(img, configs)

    @staticmethod
    def apply_noises_normal_font(img):
        """ Apply different kinds of noises defined in configs (normal fonts)
            Single config row:
                [x, y, z]
            x - max deviation from base color
            y - density of noise in percent
            z - radius of single dot
        """
        configs = [
            [
                [20, 0.7, 1],
                [100, 0.01, 7],
                [70, 0.05, 4],
            ],
            [
                [20, 0.25, 3],
                [40, 0.2, 2],
                [130, 0.01, 2],
            ],
            [
                [20, 2.2, 1],
            ]
        ]

        return DistortedTransformation.apply_noises(img, configs)

    @staticmethod
    def fish_eye(img):
        # TODO
        K = np.array([[2, 0., 3], [0., 2, 3], [0., 0., 1.]])

        # zero distortion coefficients work well for this image
        D = np.array([0., 0., 0., 0.])

        # use Knew to scale the output
        Knew = K.copy()
        Knew[(0, 1), (0, 1)] = 0.4 * Knew[(0, 1), (0, 1)]

        return cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew)

    @staticmethod
    def random_borders(image, max_border=.1, horizontal_sides_probability=.5, vertical_sides_probability=.5):
        im_height, im_width = image.shape[:2]

        borders = [0 if random.random() < horizontal_sides_probability else
                   int(random.uniform(0., max_border * im_height)) for _ in range(2)]
        borders.extend([0 if random.random() < vertical_sides_probability else
                        int(random.uniform(0., max_border * im_width)) for _ in range(2)])

        image = cv2.copyMakeBorder(image, *borders, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255, 0))

        return cv2.resize(image, (im_width, im_height), interpolation=cv2.INTER_CUBIC)

    @staticmethod
    def cut_horizontally(image, left=0, right=0, rescale=True, horizontal=True):
        im_height, im_width = image.shape[:2]

        if horizontal:
            left = int(im_width * left)
            right = int(im_width * right)
            image = image[:, left:im_width - right]
        else:
            top = int(im_height * left)
            bottom = int(im_height * right)
            image = image[top:im_height-bottom, :]

        if rescale:
            image = cv2.resize(image, (im_width, im_height), interpolation=cv2.INTER_CUBIC)

        return image

    @staticmethod
    def cut_vertically(image, top=0, bottom=0, rescale=True):
        return DistortedTransformation.cut_horizontally(image, top, bottom, rescale, horizontal=False)
