""" Generate synthetic serial number and date crops. """
import random
import numpy as np
import cv2
import aug

from ocr.aug.augmenter.augmenter import Augmenter
from ocr.aug.config import config


class CropAugmenter(Augmenter):
    def __init__(self):
        super(CropAugmenter, self).__init__(op_type="crop")

    def get_synthetic_text_crop(self):
        """ Generate random date and serial number text images using real background data. """
        if random.getrandbits(1):
            img, img_value = self.get_date_as_img()
        else:
            serial_len = random.randint(4, 20)
            img, img_value = self.get_serial_number_as_img(serial_len)

        # when generator is initialized, set font type (dotted, embossed, printed)
        self.font_type = self.generator.get_font_type()

        scale_ratio = 2
        bg_shape = int(img.shape[0]/scale_ratio), int(img.shape[1]/scale_ratio), img.shape[2]
        # get background from real data
        bg_img = self.find_background_for_crop(*random.choice(self.bg_data), bg_shape)
        if bg_img is not None:
            bg_img = cv2.resize(bg_img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)

        # apply text transformations
        ops_pipeline = self.transformation_ops[self.font_type].text_ops
        if ops_pipeline:
            img = ops_pipeline.apply(aug.Sample(image=img.copy())).image

        # if real background image has been found, use it
        if bg_img is not None:
            img = self.set_text_color(bg_img, img)
            bg_img = self.fit_image_to_shape(img, bg_img)
            img = self.add_real_background_to_synthetic_crop(img, bg_img)

        # apply composite transformations
        ops_pipeline = self.transformation_ops[self.font_type].composite_ops
        if ops_pipeline:
            img = ops_pipeline.apply(aug.Sample(image=img.copy())).image

        return img, img_value

    @staticmethod
    def fit_image_to_shape(img_ref, img):
        """ Fit image to given reference image. """
        if not np.array_equal(np.array(img_ref.shape[:2]), 2 * np.array(img.shape[:2])):
            return cv2.resize(img, (img_ref.shape[1], img_ref.shape[0]), interpolation=cv2.INTER_CUBIC)

    def set_text_color(self, bg, img):
        """ Set text color basing on average color distribution. """
        bg = cv2.cvtColor(bg, cv2.COLOR_RGB2GRAY)
        average = np.average(bg)
        if average < config.params.bright_text_threshold and not self.generator.is_dotted():
            img[:, :, :3] = 255 - img[:, :, :3]

        return img
