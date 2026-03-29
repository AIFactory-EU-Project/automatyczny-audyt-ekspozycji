""" Augments existing values detector data. """
import json
import os
import cv2
import numpy as np

from tqdm import tqdm
from multiprocessing.pool import ThreadPool

from ocr.aug.augmenter.front_augmenter import FrontAugmenter
from ocr.aug.config import config
from ocr.detection.convert_to_coco import read_categories_data, append_to_coco

DST = "/tytan/raid/neuca/data/detection/values/augs/v1"


def generate_front(augmenter, iteration, set_dir, coco_format_data, ann_counter):
    aug_img, date_pos, serial_pos = augmenter.get_synthetic_face()
    if date_pos is None or serial_pos is None:
        return

    # cv2.imshow("aug", aug_img)
    # cv2.waitKey()

    filename = f"{iteration}.jpg"
    dst_pth = os.path.join(set_dir, filename)
    cv2.imwrite(dst_pth, aug_img)

    append_to_coco(coco_format_data,
                   filename,
                   iteration,
                   *aug_img.shape[:2],
                   np.array(date_pos),
                   np.array(serial_pos),
                   ann_counter)


def augment_data(dst):
    pool = ThreadPool(processes=config.params.workers)
    front_aug = FrontAugmenter()
    classes_pth = "/tytan/raid/neuca/data/detection/values/classes.json"

    train_iterations = int(config.params.front_gen_iterations * config.params.train_ratio)
    val_iterations = config.params.front_gen_iterations - train_iterations
    for set_name, iterations in zip(["train", "validation"], [train_iterations, val_iterations]):
        coco_format_data = {
            "images": [],
            "annotations": [],
            # define a single class for detection without classification (required by the coco format)
            "categories": read_categories_data(classes_pth)
        }
        set_dir = os.path.join(dst, set_name)
        if not os.path.exists(set_dir):
            os.makedirs(set_dir)

        anno_dir = os.path.join(dst, "annotations")
        if not os.path.exists(anno_dir):
            os.makedirs(anno_dir)

        def gen(iteration):
            generate_front(front_aug, iteration, set_dir, coco_format_data, ann_counter)

        ann_counter = {"count": 0}
        for _ in tqdm(pool.imap_unordered(gen, range(iterations)), total=iterations):
            pass

        with open(os.path.join(anno_dir, f"{set_name}.json"), "w") as f:
            json.dump(coco_format_data, f)


if __name__ == '__main__':
    augment_data(DST)
