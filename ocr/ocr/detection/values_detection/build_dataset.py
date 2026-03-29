import copy
import glob
import json
import os
import random
import re
import cv2
import numpy as np

from collections import defaultdict


from ocr.detection.convert_to_coco import save_subset_in_coco_format, read_categories_data, append_to_coco

SRC_DIR = "/tytan/raid/neuca/data/orig/tagger_data"
DST_DIR = "/tytan/raid/neuca/data/detection/values/v1"
SPLIT = {
    "train": .9,
    "val": .1,
    "test": "former"  # use former data as a test data
}


def split_into_subsets(json_data, split):
    """ Split data into three subsets.

    :param json_data: A JSON object containing original data.
    :param split: A dictionary describing sizes of subsets.
    :return: 3 lists: train, validation, test.
    """
    test_data = []
    for entry in copy.deepcopy(json_data):
        if split["test"] in entry["localPath"]:
            test_data.append(entry)
            json_data.remove(entry)

    train_idx = int(len(json_data) * split["train"])
    validation_idx = int(len(json_data) * (split["val"] + split["train"]))

    return json_data[:train_idx], json_data[train_idx:validation_idx], test_data


def build(src, dst, split):
    """ Build dataset for values detector training.

    :param src: A path to the source directory.
    :param dst: A path to the destination directory.
    :param split: A dictionary describing sizes of subsets.
    """

    json_data = []
    for json_pth in glob.iglob(os.path.join(src, "**/*.json"), recursive=True):
        with open(json_pth) as f:
            json_data.extend(json.load(f))

    classes_pth = "/tytan/raid/neuca/data/detection/values/classes.json"
    train_subset, validation_subset, test_subset = split_into_subsets(json_data, split)
    save_subset_in_coco_format(train_subset, dst, classes_pth, split_name="train")
    save_subset_in_coco_format(validation_subset, dst, classes_pth, split_name="validation")
    save_subset_in_coco_format(test_subset, dst, classes_pth, split_name="test")


def split_aug_original_data(srcs):
    """ Split original and augmented data.

    :param srcs: A list of paths to the source directories.
    :return Two lists containing paths to augmented and original data.
    """
    aug = []
    orig = []
    for src in srcs:
        if "aug" in src:
            aug.append(src)
        else:
            orig.append(src)

    return aug, orig


def read_data_from_annos(pths):
    """ Read annotation data for given paths.

    :param pths: A list of paths to the source directories.
    :return A list of defaultdicts in the following format: subset -> [list of {img_pth->img_annotations} pairs}].
    """
    all_data = []
    for pth in pths:
        data = {}
        annos_pth = os.path.join(pth, "annotations")
        for json_pth in glob.iglob(os.path.join(annos_pth, "*.json")):
            subset_name = os.path.basename(json_pth).split(".")[0]
            with open(json_pth, "r") as f:
                json_data = json.load(f)

            subset_data = defaultdict(list)
            start = 0
            for img_dict in json_data["images"]:
                img_anno = []
                for anno_dict in json_data["annotations"][start:]:
                    if anno_dict["image_id"] != img_dict["id"]:
                        break
                    a_bbox = [int(b) for b in anno_dict["bbox"]]
                    # annotations contain xmin, ymin, width, height
                    x_min, y_min = a_bbox[0], a_bbox[1]
                    width, height = a_bbox[2], a_bbox[3]
                    img_anno.append([[x_min, y_min], [x_min+width, y_min],
                                     [x_min+width, y_min+height], [x_min, y_min+height]])
                    start += 1

                if img_anno:
                    img_pth = os.path.join(pth, subset_name, img_dict["file_name"])
                    subset_data[img_pth] = img_anno

            data[subset_name] = subset_data
        all_data.append(data)

    return all_data


def build_balanced(srcs, dst):
    """ Build balanced dataset for values detector training.

    :param srcs: A list of paths to datasets to be balanced (multiple augs and one original).
    :param dst: A path to the destination directory.
    """
    aug, original = split_aug_original_data(srcs)
    # there should be only one original path
    assert len(original) == 1

    augmentations = read_data_from_annos(aug)
    original = read_data_from_annos(original)[0]

    for i, aug in enumerate(augmentations):
        for subset in ["train", "validation", "test"]:
            data = aug.get(subset, None)
            ann_counter = {"count": 0}
            coco_format_data = {
                "images": [],
                "annotations": [],
                # define a single class for detection without classification (required by the coco format)
                "categories": read_categories_data("/tytan/raid/neuca/data/detection/values/classes.json")
            }
            sub_dir = os.path.join(dst, subset)
            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)

            anno_dir = os.path.join(dst, "annotations")
            if not os.path.exists(anno_dir):
                os.makedirs(anno_dir)

            data_iter = 0
            orig_suffix = 0

            def append(img_pth, img_data, suffix=i):
                img = cv2.imread(img_pth)
                filename, ext = os.path.basename(img_pth).split(".")
                filename += f":{str(suffix)}.{ext}"
                dst_pth = os.path.join(dst, subset, filename)
                os.symlink(img_pth, dst_pth)
                if len(img_data) == 1:
                    img_data.append([[0, 0], [0, 0], [0, 0], [0, 0]])
                append_to_coco(coco_format_data, filename, data_iter, *img.shape[:2], *np.array(img_data), ann_counter)

            if data is None and original.get(subset, None):
                for img_pth, img_data in original[subset].items():
                    append(img_pth, img_data)
                    data_iter += 1

            if data:
                for img_pth, img_data in data.items():
                    append(img_pth, img_data)
                    data_iter += 1
                    if random.random() < .4:
                        img_pth, img_data = random.choice(list(original[subset].items()))
                        append(img_pth, img_data, suffix=orig_suffix)
                        orig_suffix += 1
                        data_iter += 1

            with open(os.path.join(anno_dir, f"{subset}.json"), "w") as f:
                json.dump(coco_format_data, f, indent=4)


def build_legacy(src, dst):
    """ Build legacy dataset for values detector training.

    :param src: A path to the source directory (built via build_from_former.py).
    :param dst: A path to the destination directory.
    """
    with open(os.path.join(src, "annotations.json"), "r") as f:
        json_data = json.load(f)

    train_subset = []
    validation_subset = []
    for entry in json_data:
        # boxes from straight1 dataset with names starting with digit 8 and 9 were used as validation set
        if re.match("(.*)straight1/(normal|embossed|dotted)/[89]", entry["originalPhoto"]):
            validation_subset.append(entry)
        elif re.match("(.*)(straight1/(normal|embossed|dotted)/[0-7]|straight2/(normal|embossed|dotted|empty))", entry["originalPhoto"]):
            train_subset.append(entry)

    classes_pth = "/tytan/raid/neuca/data/detection/values/classes.json"
    save_subset_in_coco_format(train_subset, dst, classes_pth, split_name="train")
    save_subset_in_coco_format(validation_subset, dst, classes_pth, split_name="validation")


if __name__ == '__main__':
    # build(SRC_DIR, DST_DIR, SPLIT)

    sources = [
        "/tytan/raid/neuca/data/detection/values/legacy",
        "/tytan/raid/neuca/data/detection/values/aug13"
    ]
    dst = "/tytan/raid/neuca/data/detection/values/balanced_legacy"
    build_balanced(sources, dst)

    # src = "/tytan/raid/neuca/data/orig/former_data/_former"
    # dst = "/tytan/raid/neuca/data/detection/values/legacy"
    # build_legacy(src, dst)
