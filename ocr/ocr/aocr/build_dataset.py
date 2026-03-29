import copy
import glob
import json
import os
import wget

SRC_DIR = "/tytan/raid/neuca/data/orig/tagger_data"
DST_DIR = "/tytan/raid/neuca/data/aocr/v1"
SPLIT = {
    "train": .9,
    "val": .1,
    "test": "former"  # use former data as a test data
}

STATUS_DONE = 2  # tagger STATUS_DONE indicates valid data


def split_into_subsets(json_data, split):
    test_data = []
    for entry in copy.deepcopy(json_data):
        if split["test"] in entry["originalPhoto"]:
            test_data.append(entry)
            json_data.remove(entry)

    train_idx = int(len(json_data) * split["train"])
    validation_idx = int(len(json_data) * (split["val"] + split["train"]))

    return json_data[:train_idx], json_data[train_idx:validation_idx], test_data


def append_data_to_labels(entry, subset_dir, labels, data_type):
    orig_name, ext = os.path.basename(entry["localPath"]).split(".")
    dst_pth = os.path.join(subset_dir, "{}_{}.{}".format(orig_name, data_type, ext))
    series_photo_location = entry["{}DataPhoto".format(data_type)]
    if "http" in series_photo_location:
        wget.download(series_photo_location, dst_pth)
    else:
        # extension of the cropped photo may be different than the original one
        dst_ext = os.path.splitext(dst_pth)[1]
        real_ext = os.path.splitext(series_photo_location)[1]
        dst_pth = dst_pth.replace(dst_ext, real_ext)
        os.symlink(series_photo_location, dst_pth)
    labels[dst_pth] = entry["{}Text".format(data_type)]


def build(src, dst, split):
    json_data = []
    for json_pth in glob.iglob(os.path.join(src, "**/*.json"), recursive=True):
        with open(json_pth) as f:
            json_data.extend(json.load(f))

    subsets = split_into_subsets(json_data, split)

    for subset, phase in list(zip(subsets, ["train", "val", "test"])):
        subset_dir = os.path.join(dst, phase)
        if not os.path.exists(subset_dir):
            os.makedirs(subset_dir)

        labels = {}
        for entry in subset:
            # append only valid and non-empty data
            if entry["seriesDataStatus"] == STATUS_DONE and entry["seriesTextStatus"] == STATUS_DONE:
                append_data_to_labels(entry, subset_dir, labels, "series")
            if entry["dateDataStatus"] == STATUS_DONE and entry["dateTextStatus"] == STATUS_DONE:
                append_data_to_labels(entry, subset_dir, labels, "date")

        with open(os.path.join(subset_dir, "annotations.json"), "w") as f:
            json.dump(labels, f)


if __name__ == '__main__':
    build(SRC_DIR, DST_DIR, SPLIT)
