""" Convert OCR aug data structure from former one kept on /kolos/storage/ocr/m2/data/ to the json containing path-label pairs. """
import json
import os
import glob
import random
import cv2

SRC = "/tytan/raid/neuca/data/orig/former_data/"
DST = "/tytan/raid/neuca/data/aocr/"
AUGS = ["aug13", "aug15"]   # augmentation sets that we want to convert
SPLIT = {
    "train": .9,
    "val": .1
}


def append_to_labels(json_pth, all_labels):
    """
    Add data to the list of data to be converted.

    :param json_pth: A path to the json defining metadata from the box (old format).
    :param all_labels: A list of data to be converted.
    """
    with open(json_pth, "r") as f:
        json_data = json.load(f)

    json_dir = os.path.dirname(json_pth)
    crop_dir = json_dir.replace("tags", "crop")
    json_name, _ = os.path.basename(json_pth).split(".")
    serial_pth = os.path.join(crop_dir, json_name + "_serial.png")
    date_pth = os.path.join(crop_dir, json_name + "_date.png")

    if cv2.imread(serial_pth) is not None:
        all_labels.append((serial_pth, json_data["SERIAL_NUMBER_VALUE"]))

    if cv2.imread(date_pth) is not None:
        all_labels.append((date_pth, json_data["DATE_VALUE"]))


def build_from_former(src, dst, augs, split):
    """ Build aug data from the old format to the new one - ready for training.

    :param src: A source directory where data is kept in the old format.
    :param dst: A destination directory where data is kept in the new format (path-label pairs).
    :param augs: A list of augmentation names to convert.
    :param split: A dictionary defining the size of subsets.
    """
    for aug_set in augs:
        all_labels = []
        aug_dir = os.path.join(dst, aug_set)
        if os.path.exists(aug_dir):
            raise Exception("Aug directory already exists - omitting!")

        os.makedirs(aug_dir)
        for json_pth in glob.iglob(f"{src}/straight*/*/*/{aug_set}/tags/*.json"):
            append_to_labels(json_pth, all_labels)

        random.shuffle(all_labels)
        train_idx = int(len(all_labels) * split["train"])
        validation_idx = int(len(all_labels) * (split["val"] + split["train"]))
        subsets = [all_labels[:train_idx], all_labels[train_idx:validation_idx]]

        for subset, phase in zip(subsets, ["train", "val"]):
            subset_dir = os.path.join(aug_dir, phase)
            if not os.path.exists(subset_dir):
                os.makedirs(subset_dir)

            labels = {}
            for orig_pth, value in subset:
                box_id = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(orig_pth))))
                name = "{}_{}_serial.png".format(os.path.basename(orig_pth).split(".")[0], box_id)
                dst_pth = os.path.join(subset_dir, name)
                labels[dst_pth] = value
                os.symlink(orig_pth, dst_pth)

            with open(os.path.join(subset_dir, "annotations.json"), "w") as f:
                json.dump(labels, f)


if __name__ == '__main__':
    build_from_former(SRC, DST, AUGS, SPLIT)
