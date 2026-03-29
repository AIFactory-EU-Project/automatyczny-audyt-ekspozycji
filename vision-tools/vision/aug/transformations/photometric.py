""" Apply photometric transformations:
    - blur
    - brightness / darkness
    - contrast
    - linear / radial gradients
    - gauss / paper / salt / jpeg noise
    - pixelization
"""
import math
import random
import cv2
import numpy as np

from vision.aug.transformations.transformation import Transformation


class PhotometricTransformation(Transformation):
    @staticmethod
    def blur(image, blur_range_coeff=10, sigma=5, horizontal=False, vertical=False):
        max_kernel_size = max(1, int(image.shape[0]/blur_range_coeff))

        k_size = random.randint(min(3, max_kernel_size), max_kernel_size)
        k_size = k_size if k_size % 2 == 1 else k_size - 1

        if horizontal:
            return cv2.GaussianBlur(image, (k_size, 1), sigmaX=sigma, sigmaY=sigma)
        elif vertical:
            return cv2.GaussianBlur(image, (1, k_size), sigmaX=sigma, sigmaY=sigma)

        return cv2.GaussianBlur(image, (k_size, k_size), sigmaX=sigma, sigmaY=sigma)

    @staticmethod
    def brightness(image, value=90, dev=10, reversed=False):
        if reversed:
            val = np.array([-value-random.randint(0, dev)], dtype=np.float)
        else:
            val = np.array([value+random.randint(0, dev)], dtype=np.float)

        return cv2.add(image, val)

    @staticmethod
    def darkness(image, value=90, dev=10):
        return PhotometricTransformation.brightness(image, value, dev, reversed=True)

    @staticmethod
    def add_color(image, color, weight=.2):
        return cv2.addWeighted(image, 1-weight, np.append(np.array(color, dtype=np.float), 0), weight, 0)

    @staticmethod
    def contrast(image, ratio=.2):
        image = image.astype(np.uint16)
        image = image * ratio
        image[:, :, :] = np.clip(image, 0, 255)

        return image.astype(np.uint8)

    @staticmethod
    def contrast_brightness(image, c_ratio=.2, b_ratio=.2):
        return np.clip(c_ratio * (image - 128.0) + 128 + b_ratio, 0, 255).astype(np.uint8)

    @staticmethod
    def linear_gradient(image, width=False, color1=20, color2=40, reverse=False):
        image = np.int16(image)
        dim = image.shape[1] if width else image.shape[0]
        for i in range(dim):
            coeff = i / float(dim)
            if reverse:
                coeff = 1. - coeff
            diff = int((color2 - color1) * coeff)
            if width:
                image[:, i, 0:3] = np.where(image[:, i, 0:3] + color1 + diff < 255, image[:, i, 0:3] + color1 + diff, 255)
            else:
                image[i, :, 0:3] = np.where(image[i, :, 0:3] + color1 + diff < 255, image[i, :, 0:3] + color1 + diff, 255)

        return image.astype(np.uint8)

    @staticmethod
    def linear_vertical_gradient(image, color1=20, color2=40, reverse=False):
        return PhotometricTransformation.linear_gradient(image, width=False, color1=color1, color2=color2, reverse=reverse)

    @staticmethod
    def linear_horizontal_gradient(image, color1=20, color2=40, reverse=False):
        return PhotometricTransformation.linear_gradient(image, width=True, color1=color1, color2=color2, reverse=reverse)

    @staticmethod
    def apply_radial(img, center, max_distance, inner_color, outer_color, rect=False):
        tmp = np.full(img.shape, outer_color, dtype=np.uint8)
        tmp_height, tmp_width = tmp.shape[:2]
        kernel = None

        left = max(0, 0 - (center[0] - max_distance))
        top = max(0, 0 - (center[1] - max_distance))
        right = max(0, (center[0] + max_distance) - tmp_width)
        bottom = max(0, (center[1] + max_distance) - tmp_height)
        tmp = cv2.copyMakeBorder(tmp, top, bottom, left, right, cv2.BORDER_CONSTANT)

        if rect:
            if random.getrandbits(1):
                dist = random.randint(10, int(.2*tmp_width))
                cv2.rectangle(tmp, (center[0]-dist, 0), (center[0]+dist, tmp_height), inner_color, thickness=cv2.FILLED)
                k_size = dist if dist % 2 == 1 else dist - 1
                kernel = (k_size, 1)
            else:
                dist = random.randint(10, int(.2*tmp_height))
                cv2.rectangle(tmp, (0, center[1]-dist), (tmp_width, center[1]+dist), inner_color, thickness=cv2.FILLED)
                k_size = dist if dist % 2 == 1 else dist - 1
                kernel = (1, k_size)
        else:
            cv2.circle(tmp, (center[0] + left, center[1] + top), int(max_distance / 1.5), inner_color, thickness=cv2.FILLED)

        kernel = kernel if kernel else (max_distance, max_distance)
        tmp = cv2.blur(tmp, kernel, borderType=cv2.BORDER_CONSTANT)
        tmp = tmp[top:tmp.shape[0]-bottom, left:tmp.shape[1]-right]

        return np.clip(img.astype(np.uint16) + tmp.astype(np.uint16), 0, 255).astype(np.uint8)

    @staticmethod
    def radial_gradient_effect(img, inner_color=150, outer_color=30, center=None, max_distance=None, rect=False, random_distance=False):
        """
            img: an input image
            center: the brightest point
            inner_color: color of the brightest point
            outer_color: color of the darkest point (localized in one of 4 corners)
            max_distance: distance between center and corner
        """
        im_height, im_width, im_depth = img.shape
        inner_color = im_depth*[inner_color]
        outer_color = im_depth*[outer_color]

        if center is None:
            center = random.randint(0, im_height), random.randint(0, im_width)

        if not rect:
            if max_distance is None:
                if random_distance:
                    size = max(im_width, im_height)
                    max_distance = size * random.uniform(.1, .3)
                else:
                    max_distance = 0
                    corners = [(0, 0), (im_height, 0), (0, im_width), (im_height, im_width)]
                    for corner in corners:
                        distance = math.sqrt((corner[0] - center[0]) ** 2 + (corner[1] - center[1]) ** 2)
                        max_distance = max(distance, max_distance)

        return PhotometricTransformation.apply_radial(img, center, int(max_distance), inner_color, outer_color, rect=rect)

    @staticmethod
    def reflection_effect(image, reflection, reflection_ratio=.5, reflection_weight=0.2):
        """ Simulate mirror reflection by merging two images """
        img_weight = 1 - reflection_weight
        if reflection_ratio == 1.:
            reflection = cv2.resize(reflection, (image.shape[1], image.shape[0]))
            reflected_roi = cv2.addWeighted(image, img_weight, reflection, reflection_weight, 0)
            return reflected_roi

        y_min, y_max, x_min, x_max = Transformation.find_random_rect(reflection_ratio, *image.shape[:2])
        reflection = cv2.resize(reflection, (x_max - x_min, y_max - y_min))
        reflected_roi = cv2.addWeighted(image[y_min:y_max, x_min:x_max], img_weight, reflection, reflection_weight, 0)
        image[y_min:y_max, x_min:x_max] = reflected_roi
        return image
    
    @staticmethod
    def gauss_noise(image, avg=0, std_dev=30):
        img_cpy = image.copy()
        try:
            m = tuple(image.shape[2]*[avg])
            s = tuple(image.shape[2]*[std_dev])
        except KeyError:
            m = avg
            s = std_dev

        cv2.randn(img_cpy, m, s)

        return cv2.add(img_cpy, image)

    @staticmethod
    def pepper_noise(image, percent=0.0005, value=None):
        if value is None:
            value = [0, 0, 0]

        percent = int(percent * image.size)
        for _ in range(percent):
            image[random.randint(0, image.shape[0] - 1), random.randint(0, image.shape[1] - 1), :] = value

        return image

    @staticmethod
    def salt_noise(image, percent=0.0005, value=None):
        if value is None:
            value = [255, 255, 255]

        return PhotometricTransformation.paper_noise(image, percent, value)

    @staticmethod
    def jpeg_noise(image, quality=90):
        _, buff = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

        return cv2.imdecode(buff, cv2.IMREAD_COLOR)

    @staticmethod
    def pixelize(image, ratio=1.5):
        im_height, im_width = image.shape[:2]
        tmp_w, tmp_h = int(im_width/ratio), int(im_height/ratio)

        image = cv2.resize(image, (tmp_w, tmp_h), interpolation=cv2.INTER_NEAREST)
        image = cv2.resize(image, (im_width, im_height), interpolation=cv2.INTER_NEAREST)

        return image

    @staticmethod
    def adjust_gamma(image, gamma=4.4):
        # TODO
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255
                          for i in np.arange(0, 256)]).astype(np.uint8)

        return cv2.LUT(image, table)

    @staticmethod
    def adjust_darkness(img, thresh=100):
        if np.average(img) < thresh:
            extra_brightness = (30, 80)

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            value = int(random.randint(*extra_brightness))
            hsv = hsv.astype(np.uint16)
            hsv[:, :, 2] = np.where(hsv[:, :, 2] + value <= 255, hsv[:, :, 2] + value, 255)
            hsv = hsv.astype(np.uint8)
            img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        return img


def main():
    lena = cv2.imread('../manager/lena.jpg')
    cv2.imshow('lena', lena)
    cv2.waitKey()

    lena = PhotometricTransformation().jpeg_noise(image=lena, quality=5)
    cv2.imshow('lena', lena)
    cv2.waitKey()


if __name__ == "__main__":
    main()
