""" Build clean images dataset from former one kept on /kolos/storage/ocr/m2/data/. """
import json
import os
import glob
import cv2
import numpy as np

from vision.helpers import file_helpers

SRC = "/tytan/raid/neuca/data/orig/former_data"
DST = "/tytan/raid/neuca/data/orig/_augmentables/backgrounds"


def build_clean(src, dst):
    """
    Create dataset of clean images used for augmentation.

    :param src: A source directory where data is kept in the old format.
    :param dst: A destination directory where data is used for augmentation.
    """
    if os.path.exists(dst):
        raise Exception("Data directory already exists - omitting!")

    os.makedirs(dst)
    labels = {}
    mappings = {}
    i = 0
    # take all original samples (667)
    for json_pth in glob.iglob(f"{src}/straight*/*/*//tags/*.json"):
        with open(json_pth, "r") as f:
            json_data = json.load(f)

        json_dir = os.path.dirname(json_pth)
        clean_dir = json_dir.replace("tags", "clean")
        if not os.path.exists(clean_dir):
            continue

        clean_pths = file_helpers.find_all_images(clean_dir)
        # exactly one clean image is expected
        assert len(clean_pths) == 1
        clean_pth = clean_pths[0]
        img = cv2.imread(clean_pth)
        if img is None:
            continue

        im_height, im_width = img.shape[:2]
        areas = np.array(json_data["AVAILABLE_AREA"])
        if areas.size == 0:
            continue

        areas[:, :, 0] *= im_width
        areas[:, :, 1] *= im_height
        areas = areas.astype(np.int).tolist()

        pth, ext = clean_pth.split(".")
        dst_pth = os.path.join(dst, f"{os.path.basename(pth)}_{i}.{ext}")
        os.symlink(clean_pth, dst_pth)
        labels[dst_pth] = areas
        mappings[dst_pth] = json_pth
        i += 1

    with open(os.path.join(dst, "labels.json"), "w") as f:
        json.dump(labels, f)

    with open(os.path.join(dst, "mapping_to_orig.json"), "w") as f:
        json.dump(mappings, f)


if __name__ == '__main__':
    build_clean(SRC, DST)
