""" Generate synthetic front face of the box. """
import logging
import os
import json
import random
import numpy as np
import cv2
import aug

from ocr.aug.augmenter.augmenter import Augmenter
from ocr.aug.augmenter.alpha_blender import AlphaBlender
from ocr.aug.transformations.embossed import emboss
from ocr.aug import aug_utils
from ocr.aug.config import config


class FrontAugmenter(Augmenter):
    def __init__(self):
        super(FrontAugmenter, self).__init__(op_type="front")
        self.bg_data = self.load_background_data()

    def load_background_data(self):
        """ Load clean images as backgrounds with additional data about original values position. """
        with open(os.path.join(self.bg_pth, "labels.json"), "r") as f:
            json_data = json.load(f)

        with open(os.path.join(self.bg_pth, "mapping_to_orig.json"), "r") as f:
            additional_data = json.load(f)

        bg_data = []
        for bg_pth, available_areas in json_data.items():
            im_h, im_w = cv2.imread(bg_pth).shape[:2]
            tags_pth = additional_data.get(bg_pth, None)
            if not tags_pth:
                continue

            with open(tags_pth, "r") as f:
                tags = json.load(f)

            def convert_areas(areas):
                areas = np.array(areas)
                if areas.size == 0:
                    return
                areas[:, :, 0] *= im_w
                areas[:, :, 1] *= im_h
                areas = areas.astype(np.int).tolist()
                # ignore invalid areas (points instead of rects)
                areas = [area for area in areas if area[0] != area[1]]
                # there should be only ONE valid data
                assert len(areas) == 1
                return areas[0]

            date_areas = convert_areas(tags["DATE"])
            serial_areas = convert_areas(tags["SERIAL_NUMBER"])
            date_areas = date_areas if date_areas else serial_areas
            serial_areas = serial_areas if serial_areas else date_areas
            bg_data.append((bg_pth, available_areas, date_areas, serial_areas))

        return bg_data

    @staticmethod
    def random_orientation(img, number_of_flips=None):
        """ Flip image n times. """
        if number_of_flips is None:
            number_of_flips = random.choice([1, 3])
        return aug_utils.flip_image(img, number_of_flips), number_of_flips

    def get_synthetic_face(self):
        """ Generate random date and serial number, find available area and insert into input image. """
        clean_img, available_areas, date_area, serial_area = random.choice(self.bg_data)
        # ignore invalid areas (points instead of rects)
        available_areas = [area for area in available_areas if area[0] != area[1]]
        clean_img = cv2.imread(clean_img)
        if clean_img is None:
            return None

        # render text images
        serial_len = random.randint(4, 20)
        date_img, serial_img = self.get_date_and_serial_number_as_img(date_area, serial_area, serial_length=serial_len)

        # when generator is initialized, set font type (dotted, embossed, printed)
        self.font_type = self.generator.get_font_type()

        img = None
        date_pos, serial_pos = None, None
        # try to insert date and serial into real, front face image
        for i in range(config.params.max_number_of_attempts):
            date_img_tmp = date_img.copy()
            serial_img_tmp = serial_img.copy()

            if random.random() < config.params.random_crop_flip:
                date_img_tmp, number_of_flips = self.random_orientation(date_img_tmp)
                serial_img_tmp, _ = self.random_orientation(serial_img_tmp, number_of_flips)

            img, date_pos, serial_pos = self.insert_date_and_serial_number(clean_img, available_areas, date_img_tmp, serial_img_tmp)
            if img is not None:
                date_pos = [date_pos, [date_pos[0] + date_img_tmp.shape[1],
                                       date_pos[1] + date_img_tmp.shape[0]]]
                serial_pos = [serial_pos, [serial_pos[0] + serial_img_tmp.shape[1],
                                           serial_pos[1] + serial_img_tmp.shape[0]]]
                break

            if i == config.params.max_number_of_attempts - 1:
                logging.warning('Attempt number: {} failed. ({} iterations)'.format(i + 1, config.params.max_number_of_attempts))

        # apply transformations if crops are inserted
        if img is not None:
            ops_pipeline = self.transformation_ops["face"].composite_ops
            if ops_pipeline:
                pipeline_ret = ops_pipeline.apply(aug.Sample(image=img.copy(), annotations=np.array([date_pos, serial_pos])))
                img = pipeline_ret.image
                date_pos, serial_pos = pipeline_ret.annotations
                date_pos = [date_pos[0].tolist(), date_pos[1].tolist()]
                serial_pos = [serial_pos[0].tolist(), serial_pos[1].tolist()]

            date_pos = [[date_pos[0][0], date_pos[0][1]],
                        [date_pos[1][0], date_pos[0][1]],
                        [date_pos[1][0], date_pos[1][1]],
                        [date_pos[0][0], date_pos[1][1]]]

            serial_pos = [[serial_pos[0][0], serial_pos[0][1]],
                          [serial_pos[1][0], serial_pos[0][1]],
                          [serial_pos[1][0], serial_pos[1][1]],
                          [serial_pos[0][0], serial_pos[1][1]]]

        return img, date_pos, serial_pos

    def insert_date_and_serial_number(self, clean_img, coords, date_crop, serial_crop):
        """ Insert crop into one of the areas with probability proportional to the size of area. """
        clean_img, pos1, pos2 = self.find_positions(clean_img, coords, date_crop, serial_crop)
        if pos1 is None or pos2 is None:
            return None, None, None

        date_crop_height, date_crop_width = date_crop.shape[:2]
        serial_crop_height, serial_crop_width = serial_crop.shape[:2]
        date_bg = clean_img[pos1[1]:pos1[1] + date_crop_height, pos1[0]:pos1[0] + date_crop_width]
        serial_bg = clean_img[pos2[1]:pos2[1] + serial_crop_height, pos2[0]:pos2[0] + serial_crop_width]

        date_crop, serial_crop = self.apply_text_transformations(date_crop, date_bg, serial_crop, serial_bg)

        alpha_blender = AlphaBlender(clean_img, self.generator, self.transformation_ops["face"])
        alpha_blender.insert_into_foreground(clean_img, date_crop, pos1)
        alpha_blender.insert_into_foreground(clean_img, serial_crop, pos2)
        composition = alpha_blender.get_composite_img()

        return composition, pos1, pos2

    def find_positions(self, img, coords, date_crop, serial_crop):
        """ Find two random positions within the given coordinates. """
        tmp_img = img.copy()
        for i in range(config.params.get_position_limiter):
            if random.random() < config.params.random_positions:
                img, pos1, pos2 = self.position_finder.get_two_unrelated_random_positions(img, coords, date_crop.shape, serial_crop.shape)
            else:
                img, pos1, pos2 = self.position_finder.get_two_related_random_positions(img, coords, date_crop.shape, serial_crop.shape)

            if pos1 is not None and pos2 is not None:
                return img, pos1, pos2

            img = tmp_img

        return img, None, None

    def apply_text_transformations(self, date_crop, date_bg, serial_crop, serial_bg):
        """ Apply the same text transformations for all data. """
        ops_pipeline = self.transformation_ops["face"].text_ops
        if ops_pipeline:
            # TODO: same transformations for date and serial
            date_crop = ops_pipeline.apply(aug.Sample(image=date_crop.copy())).image
            serial_crop = ops_pipeline.apply(aug.Sample(image=serial_crop.copy())).image

        if self.generator.get_font_type() == "embossed":
            # when the text is embossed and exactly the same transformation needed, pass a pair of images as a single image
            date_crop, serial_crop = self.apply_text_transformations_embossed(date_crop, serial_crop, date_bg, serial_bg)

        return date_crop, serial_crop

    @staticmethod
    def apply_text_transformations_embossed(date, serial, date_bg, serial_bg):
        """ Apply embossed transformation: uses cvlab-generated code. """
        txt_shape = date.shape[0] + serial.shape[0], max(date.shape[1], serial.shape[1]), 4
        bg_shape = date_bg.shape[0] + serial_bg.shape[0], max(date_bg.shape[1], serial_bg.shape[1]), 3

        joined_text = np.zeros(txt_shape, dtype=np.uint8)
        joined_background = np.zeros(bg_shape, dtype=np.uint8)
        joined_text[:] = 255
        joined_background[:] = 255

        joined_text[0:date.shape[0], 0:date.shape[1]] = date
        joined_text[date.shape[0]:date.shape[0] + serial.shape[0], 0:serial.shape[1]] = serial

        joined_background[0:date_bg.shape[0], 0:date_bg.shape[1]] = date_bg
        joined_background[date_bg.shape[0]:date_bg.shape[0] + serial_bg.shape[0], 0:serial_bg.shape[1]] = serial_bg

        # simulate embossed text
        outputs = emboss(joined_text, joined_background)
        image = outputs['o1'].value
        date = image[0:date_bg.shape[0], 0:date_bg.shape[1]]
        serial = image[date_bg.shape[0]:date_bg.shape[0] + serial_bg.shape[0], 0:serial_bg.shape[1]]
        return date, serial
