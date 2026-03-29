""" Extracting crops from boxes. """
import os
import logging
import shutil
import cv2

from glob import iglob

from ocr import utils
from vision.helpers import file_helpers


DATA_DIR = "/kolos/m2/ocr/data"


class CropsExtractor:
    def __init__(self, src_dir):
        self.file_names = utils.load_file_paths(src_dir)
        self.labels = utils.load_labels(src_dir)
        self.input_dir = src_dir
        # self.init_dir_tree(src_dir)

    @staticmethod
    def init_dir_tree(input_dir):
        for item in iglob(input_dir):
            file_helpers.makedirs((os.path.join(input_dir, item, "crop")))

    def start_job(self):
        for name in self.file_names:
            path = os.path.join(
                self.input_dir, name.split('/')[0], "front", '{}.png'.format(name.split('/')[1]))

            if not os.path.exists(path):
                logging.warning(f"{path} not found.")
                continue

            img = cv2.imread(path)
            out_dir = os.path.join(self.input_dir, name.split('/')[0], "crop")

            date_path = os.path.join(out_dir, "{}_date.png".format(name.split('/')[1]))
            serial_path = os.path.join(out_dir, "{}_serial.png".format(name.split('/')[1]))

            self.save_crop(img, name, utils.Mode.DATE.name, date_path)
            self.save_crop(img, name, utils.Mode.SERIAL_NUMBER.name, serial_path)

    def save_crop(self, img, name, crop_type, output_path):
        label = utils.get_label_if_exists(self.labels, name, crop_type)
        if label is not None:
            label = utils.convert_positions(img.shape, label)
            l, r, t, b = self.borders(label[0], img.shape)
            crop = img[t:b, l:r]
            cv2.imwrite(output_path, crop)

    @staticmethod
    def borders(date_label, shape, cut_crops_scale=1.05):
        borders = min(date_label[0][0], date_label[1][0]), max(date_label[0][0], date_label[1][0]), \
                  min(date_label[0][1], date_label[1][1]), max(date_label[0][1], date_label[1][1])

        h = borders[3] - borders[2]
        w = borders[1] - borders[0]

        scale = cut_crops_scale - 1

        return int(max(0, borders[0] - w * scale)), int(min(shape[1] - 1, borders[1] + w * scale)), \
               int(max(0, borders[2] - h * scale)), int(min(shape[0] - 1, borders[3] + h * scale))

    @staticmethod
    def delete_crops(input_dir):
        for item in os.listdir(input_dir):
            path = os.path.join(input_dir, item, "crop")
            if os.path.exists(path):
                shutil.rmtree(path)


if __name__ == "__main__":
    extractor = CropsExtractor(DATA_DIR + "/straight[123]/*")
    extractor.start_job()
