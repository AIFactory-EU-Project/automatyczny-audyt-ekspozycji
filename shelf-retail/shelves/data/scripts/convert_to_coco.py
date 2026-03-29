""" Convert files from tagger output to json files in coco format.
    References:
        * http://cocodataset.org/#format-data
        * http://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch

    Example:
    {
        "images": [
            {
                "file_name": "name.jpg",
                "height": 427,
                "width": 640,
                "id": 397133
            },
            ...
        ]
        "annotations": [
            {
                "segmentation": [[x1, y1, x2, y2, ... , xn, yn]],
                "area": <polygon area>,
                "iscrowd": 0,
                "image_id": <image_id>,
                "bbox": [x1, y1, w, h],
                "category_id": <category_id>,
                "id": <id>
            },
            ...
        ]
        "categories": [
            { "supercategory": "class_1", "id": 1, "name": "class_1" }
        ]
    }

"""

import json
import os
import random
import shutil
from glob import glob

import cv2
import numpy as np
from tqdm import tqdm

SRC_DIR = "/tytan/raid/shelf-retail/data/orig/detection/grills"
DST_DIR = "/tytan/raid/shelf-retail/data/detection/grills"
SPLIT = {
    "train": .8,
    "validation": .2,
    "test": .0
}


def convert_to_coco(src_dir, dst_dir, split=SPLIT):
    """Find all available annotations, load to single list and shuffle, then split them
        into train/validation/test subsets. Finally, create symlinks to the original images,
        convert metadata to COCO format and save in a separate file for each subset.
    """
    assert sum(list(split.values())) == 1.
    data = read_data(src_dir)
    train_subset, validation_subset, test_subset = split_into_subsets(data, split)

    save_subset_in_coco_format(train_subset, dst_dir, src_dir, split_name='train')
    save_subset_in_coco_format(validation_subset, dst_dir, src_dir, split_name='validation')
    save_subset_in_coco_format(test_subset, dst_dir, src_dir, split_name='test')


def read_data(src_dir):
    """Find all available annotations and join them into single list.

    :param src_dir: A path to directory tree that will be searched.
    :return: A list of all available samples.
    """
    paths = []
    for name in ["via_region_data.json", "annotations.json"]:
        paths.extend(list(glob("{}/**/{}".format(src_dir, name), recursive=True)))

    assert len(paths) > 0

    data = []
    for path in paths:
        with open(path) as f:
            samples = json.load(f)
            if isinstance(samples, dict):
                samples = list(samples.values())

            for sample in samples:
                sample['file_path'] = os.path.join(os.path.dirname(path), sample['filename'])

            data.extend(samples)

    assert len(data) > 0

    print("{} samples found.".format(len(data)))

    return data


def split_into_subsets(samples, split):
    """Split a list of samples into 3 subsets: train, validation, test.

    :param samples: A list of samples in original format.
    :param split: A dictionary describing sizes of subsets.
    :return: 3 lists: train, validation, test.
    """
    random.shuffle(samples)

    train_idx = int(len(samples) * split['train'])
    validation_idx = int(len(samples) * (split['validation'] + split['train']))

    return samples[:train_idx], samples[train_idx:validation_idx], samples[validation_idx:]


def save_subset_in_coco_format(samples, dst_dir, src_dir, split_name):
    """Convert format from tagger output to coco for single subset (train/validation/test).

    :param samples: A list of samples in original format.
    :param dst_dir: A directory, where symlinks and metadata files will be created.
    :param src_dir: A path to the root source directory.
    :param split_name: Name of current split.
    """
    # Prepare dictionary compatible with COCO format
    ann_counter = 0
    coco_format_data = {
        'images': [],
        'annotations': [],

        # Define a single class for detection without classification
        #   (required by the coco format)
        'categories': read_categories_data(os.path.join(src_dir, "classes.json"))
    }

    # Prepare destination directory
    output_split_dir = os.path.join(dst_dir, split_name)
    anno_dir = os.path.join(dst_dir, "annotations")
    if os.path.exists(output_split_dir):
        shutil.rmtree(output_split_dir)

    os.makedirs(output_split_dir)

    if not os.path.exists(anno_dir):
        os.makedirs(anno_dir)

    for i, sample in tqdm(enumerate(samples), desc=split_name):
        path = sample['file_path'].replace(".JPG", ".jpg")

        # Create symbolic link to image
        dst_name = "{:012d}.{}".format(i, os.path.basename(path))
        dst_path = os.path.join(output_split_dir, dst_name)
        os.symlink(path, dst_path)

        img = cv2.imread(path)

        if img is None:
            print('Warning! File "{}" does not exist.'.format(path))
            continue

        height, width = img.shape[:2]

        # Add description of current image
        coco_format_data["images"].append({
            "file_name": dst_name,
            "id": i,
            "height": height,
            "width": width,
        })

        if isinstance(sample["regions"], dict):
            sample["regions"] = list(sample["regions"].values())

        for region in sample["regions"]:
            category_id = 1

            if region.get("shape_attributes", None):
                # if no label is specified in anno data, then we detect only one object
                category_id = int(region['region_attributes'].get("label", 1))
                region = region["shape_attributes"]

            x = region["x"]
            y = region["y"]
            w = region["width"]
            h = region["height"]
            points = np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])
            points = counterclockwise_order(points).astype(np.float32)

            coco_format_data["annotations"].append({
                "id": ann_counter,
                "image_id": i,
                "category_id": category_id,
                "segmentation": [points.flatten().tolist()],
                "area": polygon_area(points),
                "bbox": bbox(points),
                "iscrowd": 0
            })

            ann_counter += 1

            # Display annotations (debug purposes)
            # pts = np.array(points, np.int32)
            # pts = pts.reshape((-1, 1, 2))
            # cv2.polylines(img, [pts], True, (0, 255, 255))
            # cv2.imshow('img', img)
            # cv2.waitKey()

    with open(os.path.join(anno_dir, "{}.json".format(split_name)), 'w') as f:
        json.dump(coco_format_data, f, indent=4)


def read_categories_data(filepath):
    """
    Return categories used for training.

    :param filepath: A path to the file containing categories data.
    :return: A list of training categories.
    """
    categories = []
    with open(filepath, "r") as f:
        json_data = json.load(f)

    for supercategory, v in json_data.items():
        for category_id, category_name in v.items():
            categories.append({"supercategory": supercategory, "id": int(category_id), "name": category_name})

    return categories


def bbox(points):
    """Return bounding box of an array of points.

    :param points: An array of points with shape (x, 2).
    """
    points = np.array(points)
    min_x, min_y = np.min(points, axis=0)
    max_x, max_y = np.max(points, axis=0)

    return float(min_x), float(min_y), float(max_x - min_x), float(max_y - min_y)


def polygon_area(points):
    """Return an area of a polygon described by a set of points
        (references: https://en.wikipedia.org/wiki/Shoelace_formula).

    :param points: An array of points with shape (x, 2).
    """
    points = np.array(points).reshape(-1, 2)

    area = 0
    q = points[-1]
    for p in points:
        area += p[0] * q[1] - p[1] * q[0]
        q = p

    return abs(area / 2)


def counterclockwise_order(points):
    """Make sure that points are in a counterclockwise order.

    :param points: An array of points with shape (x, 2).
    :return: An array of transformed points.
    """
    sum = 0
    points = np.array(points).reshape(-1, 2)

    for i, point in enumerate(points):
        next_index = i + 1 if i + 1 < len(points) else 0
        sum += (points[next_index][0] - points[i][0]) * (points[i][1] + points[next_index][1])

    if sum > 0:
        # Flip points to counterclockwise order
        points = np.flip(points, 0)

    return points


if __name__ == '__main__':
    convert_to_coco(SRC_DIR, DST_DIR, SPLIT)
