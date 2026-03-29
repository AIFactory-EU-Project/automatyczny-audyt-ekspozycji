""" Convert front aug data structure from former one kept on /kolos/storage/ocr/m2/data/ to the COCO format used by detector. """
import json
import os
import glob
import cv2
import numpy as np

from ocr.detection.convert_to_coco import read_categories_data, append_to_coco

SRC = "/tytan/raid/neuca/data/orig/former_data"
DST = "/tytan/raid/neuca/data/detection/values"
AUGS = ["aug13"]   # augmentation sets that we want to convert


def build_from_former(src, dst, augs):
    """ Build aug data from the old format to the new one - ready for training.

    :param src: A source directory where data is kept in the old format.
    :param dst: A destination directory where data is kept in the new format (path-label pairs).
    :param augs: A list of augmentation names to convert.
    """
    for aug_set in augs:
        aug_dir = os.path.join(dst, aug_set)
        if os.path.exists(aug_dir):
            raise Exception("Aug directory already exists - omitting!")

        os.makedirs(aug_dir)
        anno_dir = os.path.join(aug_dir, "annotations")
        if not os.path.exists(anno_dir):
            os.makedirs(anno_dir)

        ann_counter = {"count": 0}
        coco_format_data = {
            "images": [],
            "annotations": [],
            # define a single class for detection without classification (required by the coco format)
            "categories": read_categories_data("/tytan/raid/neuca/data/detection/values/classes.json")
        }

        for i, json_pth in enumerate(glob.iglob(f"{src}/straight*/*/*/{aug_set}/tags/*.json")):
            with open(json_pth, "r") as f:
                json_data = json.load(f)

            json_dir = os.path.dirname(json_pth)
            front_dir = json_dir.replace("tags", "front")
            json_name, _ = os.path.basename(json_pth).split(".")
            front_pth = os.path.join(front_dir, f"{json_name}.png")
            front_img = cv2.imread(front_pth)

            if front_img is None:
                continue

            dst_dir = os.path.join(aug_dir, "train")
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            filename = f"{json_name}_{str(i)}.png"
            dst_pth = os.path.join(dst_dir, filename)
            os.symlink(front_pth, dst_pth)

            im_height, im_width = front_img.shape[:2]
            # there is exactly one annotation for each value
            date_pos = np.array(json_data["DATE"][0])
            date_pos[:, 0] *= im_width
            date_pos[:, 1] *= im_height
            date_pos = date_pos.astype(np.int)

            serial_pos = np.array(json_data["SERIAL_NUMBER"][0])
            serial_pos[:, 0] *= im_width
            serial_pos[:, 1] *= im_height
            serial_pos = serial_pos.astype(np.int)

            date_pos = [[date_pos[0][0], date_pos[0][1]],
                        [date_pos[1][0], date_pos[0][1]],
                        [date_pos[1][0], date_pos[1][1]],
                        [date_pos[0][0], date_pos[1][1]]]

            serial_pos = [[serial_pos[0][0], serial_pos[0][1]],
                          [serial_pos[1][0], serial_pos[0][1]],
                          [serial_pos[1][0], serial_pos[1][1]],
                          [serial_pos[0][0], serial_pos[1][1]]]

            append_to_coco(coco_format_data, filename, i, im_height, im_width, date_pos, serial_pos, ann_counter)

        with open(os.path.join(anno_dir, "train.json"), "w") as f:
            json.dump(coco_format_data, f)


if __name__ == '__main__':
    build_from_former(SRC, DST, AUGS)
