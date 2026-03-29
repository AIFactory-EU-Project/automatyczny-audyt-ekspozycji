import json
import os
import shutil
import cv2
import numpy as np

from tqdm import tqdm

from ocr.scanner.tester import rotate_bound


STATUS_DONE = 2  # tagger STATUS_DONE indicates valid data


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


def append_to_coco(coco_format_data, file_name, file_id, file_height, file_width, date_area, serial_area, ann_counter):
    """ Append entry to coco format.

     :param coco_format_data: A JSON object representing coco format.
     :param file_name: A name of entry.
     :param file_id: An ID of entry.
     :param file_height: A height of entry.
     :param file_width: A width of entry.
     :param date_area: An array representing bounding box of date.
     :param serial_area: An array representing bounding box of serial number.
     :param ann_counter: An object representing annotations' counter (ID of annotation).
     """
    coco_format_data["images"].append({
        "file_name": file_name,
        "id": file_id,
        "height": file_height,
        "width": file_width,
    })

    def add_to_annotations(area):
        area = counterclockwise_order(area).astype(np.float32)
        coco_format_data["annotations"].append({
            "id": ann_counter["count"],
            "image_id": file_id,
            "category_id": 1,
            "segmentation": [area.flatten().tolist()],
            "area": polygon_area(area),
            "bbox": bbox(area),
            "iscrowd": 0
        })

        return 1

    ann_counter["count"] += add_to_annotations(date_area)
    ann_counter["count"] += add_to_annotations(serial_area)


def save_subset_in_coco_format(samples, dst_dir, classes_pth, split_name):
    """Convert format from tagger output to coco for single subset (train/validation/test).

    :param samples: A list of samples in original format.
    :param dst_dir: A directory, where symlinks and metadata files will be created.
    :param split_name: Name of current split.
    :param classes_pth: A path to the classes.json file to read categories.
    """
    # prepare dictionary compatible with COCO format
    ann_counter = {"count": 0}
    coco_format_data = {
        'images': [],
        'annotations': [],
        # define a single class for detection without classification (required by the coco format)
        'categories': read_categories_data(classes_pth)
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
        path = sample["localPath"].replace(".JPG", ".jpg")
        box_area = sample["boxArea"]
        if not box_area and sample.get("detectionGeneralStatus", None) != STATUS_DONE:
            path = sample["boxPhoto"] if "https" not in sample["boxPhoto"] else path
            box_area = {"x": 0, "y": 0, "width": 0, "height": 0, "rotate": 0}

        img = cv2.imread(path)
        if img is None:
            print('Warning! File "{}" does not exist.'.format(path))
            continue

        filename, ext = os.path.basename(path).split(".")
        filename = f"{filename}:{str(i)}.{ext}"
        dst_path = os.path.join(output_split_dir, filename)
        angle = box_area["rotate"]
        box_x, box_y, = box_area["x"], box_area["y"]
        if angle:
            img = rotate_bound(img, angle)
            cv2.imwrite(dst_path, img)
        else:
            # create symbolic link to image
            os.symlink(path, dst_path)

        def transform_area(area):
            """ Transform points to reflect coordinates on the whole image instead of box roi.

            :param area: A JSON object representing bounding box.
            """
            # no date nor serial number
            if not area:
                return np.array([(0, 0), (0, 0), (0, 0), (0, 0)])

            x, y, = area["x"] + box_x, area["y"] + box_y
            w, h = area["width"], area["height"]
            points = np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])
            return points

        serial_area = transform_area(sample["seriesDataArea"])
        date_area = transform_area(sample["dateDataArea"])

        # append to coco annotations
        append_to_coco(coco_format_data, filename, i, *img.shape[:2], serial_area, date_area, ann_counter)

    with open(os.path.join(anno_dir, "{}.json".format(split_name)), 'w') as f:
        json.dump(coco_format_data, f, indent=4)
