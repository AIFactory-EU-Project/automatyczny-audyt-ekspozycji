import copy
import glob
import json
import os

from shelves.data.mappings.sku_mappings import sku_mapping

SRC_DIR = "/tytan/raid/shelf-retail/data/orig/classification/meals"
DST_DIR = "/tytan/raid/shelf-retail/data/classification/v05_tmp"
SPLIT = {
    "validation": [10, 11],
    "test": [7, 8, 15, 16]
}


def split_into_subsets(json_data, split):
    val_data = []
    test_data = []
    for entry in copy.deepcopy(json_data):
        set_number = entry["originalPhotoFilename"].split(".")[2]
        if int(set_number) in split["test"]:
            test_data.append(entry)
            json_data.remove(entry)
        if int(set_number) in split["validation"]:
            val_data.append(entry)
            json_data.remove(entry)

    return [json_data, val_data, test_data]


def build(src_dir, dst_dir, split):
    json_data = []
    for json_pth in glob.iglob(os.path.join(src_dir, "**/*.json"), recursive=True):
        with open(json_pth) as f:
            json_data.extend(json.load(f))

    subsets = split_into_subsets(json_data, split)

    for subset, phase in list(zip(subsets, ["train", "val", "test"])):
        subset_dir = os.path.join(dst_dir, phase)
        if not os.path.exists(subset_dir):
            os.makedirs(subset_dir)

        labels = {}
        for entry in subset:
            # status 6 -> SKU not present on the image
            if entry["status"] == 6:
                continue

            class_idx = entry["skuIdx"]
            # status 5 -> SKU not on the list of recognizable SKUs
            # status 7 -> SKU cannot be identified
            if not class_idx and entry["status"] in [5, 7]:
                class_names = ["Unknown"]
            else:
                class_names = sku_mapping.get(class_idx, None)
            if not class_names:
                raise Exception("{} - no such sku idx!\n{}".format(class_idx, entry["localPath"]))

            # if SKU was marked as general, use only general class name
            is_general = entry["generalClass"]
            if is_general and class_idx:
                class_names = [entry["generalClassName"]]

            dst_pth = os.path.join(subset_dir, os.path.basename(entry["localPath"]))
            os.symlink(entry["localPath"], dst_pth)
            labels[dst_pth] = class_names

        with open(os.path.join(subset_dir, "labels.json"), "w") as f:
            json.dump(labels, f)


if __name__ == "__main__":
    build(SRC_DIR, DST_DIR, SPLIT)
