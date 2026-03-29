""" Augments existing OCR data. """
import json
import cv2
import os
import aug

from tqdm import tqdm
from multiprocessing.pool import ThreadPool

from ocr.aug.config import config
from ocr.aug.transformations.configs.ocr_pipelines import OcrPipeline
from vision.helpers import file_helpers

SRC = "/tytan/raid/neuca/data/aocr/v1"
DST = "/tytan/raid/neuca/data/aocr/augs/v1"


def augment_file(img_pth, img_value, set_dir, set_labels):
    augmentations = []
    for j in range(config.params.augmented_per_real_number):
        img = cv2.imread(img_pth)
        pipeline = OcrPipeline()
        augmented = pipeline.apply(aug.Sample(img)).image
        if augmented is None:
            continue
        augmentations.append(augmented)

    for i, img in enumerate(augmentations):
        img_name, img_ext = os.path.basename(img_pth).split(".")
        img_name += f":aug{str(i)}.{img_ext}"
        if not os.path.exists(set_dir):
            os.makedirs(set_dir)
        dst_pth = os.path.join(set_dir, img_name)
        cv2.imwrite(dst_pth, img)
        set_labels[dst_pth] = img_value


def augment_data(src, dst):
    pool = ThreadPool(processes=config.params.workers)

    to_augment = {}
    subdirs = os.listdir(src)
    for subdir in subdirs:
        json_pth = file_helpers.find_all_jsons(os.path.join(src, subdir))[0]
        to_augment[subdir] = json_pth

    for set_name, json_pth in to_augment.items():
        with open(json_pth, "r") as f:
            json_data = json.load(f)

        set_labels = {}
        set_dir = os.path.join(dst, set_name)

        def aug(pair):
            pth, value = pair
            augment_file(pth, value, set_dir, set_labels)

        for _ in tqdm(pool.imap_unordered(aug, json_data.items()), total=len(json_data.keys())):
            pass

        with open(os.path.join(set_dir, "annotations.json"), "w") as f:
            json.dump(set_labels, f)


if __name__ == '__main__':
    augment_data(SRC, DST)
