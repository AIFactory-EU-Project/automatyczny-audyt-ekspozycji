""" Base class for crop, front and dummy augmenters. """
import json
import os
import cv2
import aug

from ocr.aug.aug_utils import apply_scale
from ocr.aug.word_generators.cropped_generator import CroppedTextGenerator
from ocr.aug.augmenter.position_finder import PositionFinder
from ocr.aug.augmenter.font_configs import DottedConfig, EmbossedConfig, PrintedConfig, FrontFaceConfig


class Augmenter:
    def __init__(self, op_type="front"):
        # augmentation operation type (front, crop or dummy)
        self.op_type = op_type
        self.font_type = "normal"
        # transformation ops for specific font type
        self.transformation_ops = {
            "dotted": DottedConfig(op_type),
            "embossed": EmbossedConfig(op_type),
            "normal": PrintedConfig(op_type),
            "face": FrontFaceConfig(op_type)
        }
        self.generator = CroppedTextGenerator(self.transformation_ops)
        self.position_finder = PositionFinder()
        self.bg_pth = "/tytan/raid/neuca/data/orig/_augmentables/backgrounds"
        self.bg_data = self.load_background_data()

    def load_background_data(self):
        """ Load clean images as backgrounds. """
        with open(os.path.join(self.bg_pth, "labels.json"), "r") as f:
            json_data = json.load(f)
        data = [(k, v) for k, v in json_data.items()]
        return data

    def get_date_and_serial_number_as_img(self, date_label, serial_label, serial_length=None, flip_when_vertical=True):
        """ Generate date and serial number as images, using the same font and similar transformations. """
        date_value = self.generator.get_date_value()
        serial_value = self.generator.get_serial_number_value(serial_length)

        date_rect_size = (abs(date_label[1][0]-date_label[0][0]), abs(date_label[1][1]-date_label[0][1]))
        serial_rect_size = (abs(serial_label[1][0]-serial_label[0][0]), abs(serial_label[1][1]-serial_label[0][1]))
        date_rect_size = apply_scale(date_rect_size)
        serial_rect_size = apply_scale(serial_rect_size)

        date, serial = self.generator.get_fixed_size_pair_of_crops(date_value, date_rect_size,
                                                                   serial_value, serial_rect_size, flip=flip_when_vertical)
        return date, serial

    def get_date_as_img(self):
        """ Generate date as image. """
        date_value = self.generator.get_date_value()
        return self.generator.get_processed_text_img(date_value), date_value

    def get_serial_number_as_img(self, serial_len=None):
        """ Generate serial number as image. """
        serial_value = self.generator.get_serial_number_value(serial_len)
        return self.generator.get_processed_text_img(serial_value), serial_value

    def find_background_for_crop(self, bg_pth, available_label, crop_shape):
        """ Find and cut background from clean images dataset. """
        bg = cv2.imread(bg_pth)
        _, point = self.position_finder.get_random_position(bg, available_label, crop_shape, flip=False)

        if point is not None:
            crop_bg = bg[point[1]:point[1] + crop_shape[0], point[0]:point[0] + crop_shape[1]]
            ops_pipeline = self.transformation_ops[self.font_type].background_ops
            if ops_pipeline:
                crop_bg = ops_pipeline.apply(aug.Sample(image=crop_bg.copy())).image
            return crop_bg

        return None

    def add_real_background_to_synthetic_crop(self, crop, crop_bg):
        """ Join real background and generated text image. """
        return self.generator.join_text_and_background(crop, crop_bg)
