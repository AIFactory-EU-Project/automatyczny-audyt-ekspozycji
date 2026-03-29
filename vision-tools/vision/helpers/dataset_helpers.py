import glob
import json
import os
import shutil
import random
import cv2
from vision.helpers import file_helpers, label_helpers
from vision.helpers import via_json_manipulation as via


def get_image_label_from_dataset(path):
    all_jsons = file_helpers.find_all_jsons(path)
    for json_path in all_jsons:
        with open(json_path) as fp:
            json_data = json.load(fp)
        ext = json_data["name"].split(".")[1]
        img_path = json_path.replace("labels", "images").replace("json", ext)
        img = cv2.imread(img_path, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
        yield img_path, img, json_path, json_data


def get_image_label_from_datasets(paths):
    for path in paths:
        for r in get_image_label_from_dataset(path):
            yield r


def split_into_datasets(data, train_part=.8, val_part=.1):
    """ Split given list into sublists representing consecutive datasets"""
    random.shuffle(data)
    train_limit = int(len(data) * train_part)
    val_limit = int(len(data) * (train_part + val_part))

    return data[:train_limit], data[train_limit:val_limit], data[val_limit:]


def build_splitted(src, dst, train_part=.8, val_part=.1, src_labels_file="labels.txt"):
    """ Build splitted datasets by copying images and creating labels.txt files """
    labels = label_helpers.load_labels_txt_list(os.path.join(src, src_labels_file))
    train, val, test = split_into_datasets(labels, train_part, val_part)
    datasets = [train, val, test]

    for i, set_name in enumerate(["train", "val", "test"]):
        images_dir = os.path.join(dst, set_name, "images")
        file_helpers.makedirs(images_dir)
        for path, label in datasets[i]:
            shutil.copy2(path, images_dir)
        labels = label_helpers.change_directory(datasets[i], images_dir)
        label_helpers.save_labels_txt(labels, os.path.join(dst, set_name, "labels.txt"), sort=True)


def merge_data(srcs, dst, src_labels_file="labels.txt"):
    """ Copy data from all sources into destination folder and create a single labels.txt file """
    all_labels = [item for src in srcs for item in label_helpers.load_labels_txt_list(os.path.join(src, src_labels_file))]
    file_helpers.makedirs(dst)
    for path, label in all_labels:
        shutil.copy2(path, dst)
    all_labels = label_helpers.change_directory(all_labels, dst)
    all_labels = list(set(all_labels))
    label_helpers.save_labels_txt(all_labels, os.path.join(dst, "labels.txt"), sort=True)


def merge_via_data(srcs, dst, src_labels_file="via_labels.json"):
    all_paths = (item for src in srcs for item in file_helpers.find_all_images(src))
    file_helpers.makedirs(dst)
    for path in all_paths:
        shutil.copy2(path, dst)
    via.merge_files_list([os.path.join(src, src_labels_file) for src in srcs], output_path=os.path.join(dst, "via_labels.json"))
