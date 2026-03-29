""" Generates synthetic OCR data with usage of real data backgrounds. """
import json
import os
import cv2

from multiprocessing.pool import ThreadPool
from tqdm import tqdm

from ocr.aug.augmenter.crop_augmenter import CropAugmenter
from ocr.aug.config import config


DST = "/tytan/raid/neuca/data/aocr/augs/gen/v1"


def generate_image(augmenter, iteration, set_dir, set_labels):
    img, img_value = augmenter.get_synthetic_text_crop()
    if img is None:
        return

    dst_pth = os.path.join(set_dir, f"{str(iteration)}.jpg")
    cv2.imwrite(dst_pth, img)
    set_labels[dst_pth] = img_value


def generate(dst):
    pool = ThreadPool(processes=config.params.workers)
    crop_aug = CropAugmenter()

    train_iterations = int(config.params.ocr_gen_iterations * config.params.train_ratio)
    val_iterations = config.params.ocr_gen_iterations - train_iterations
    for set_name, iterations in zip(["train", "val"], [train_iterations, val_iterations]):
        set_labels = {}
        set_dir = os.path.join(dst, set_name)
        if not os.path.exists(set_dir):
            os.makedirs(set_dir)

        def gen(iteration):
            generate_image(crop_aug, iteration, set_dir, set_labels)

        for _ in tqdm(pool.imap_unordered(gen, range(iterations)), total=iterations):
            pass

        with open(os.path.join(set_dir, "annotations.json"), "w") as f:
            json.dump(set_labels, f)


if __name__ == '__main__':
    generate(DST)
