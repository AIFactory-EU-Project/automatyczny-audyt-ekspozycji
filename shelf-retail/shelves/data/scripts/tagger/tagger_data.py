""" Download annotated data"""

import glob
import json
import os
import wget
import tqdm
import cv2
import numpy as np

from multiprocessing.pool import ThreadPool
from shelves.data.scripts.tagger.config import *

SRC_DIR = "/tytan/raid/shelf-retail/data/orig/tagger_exports"


def transform_photo_and_anno(dst_pth, category, anno_data):
    set_number = os.path.basename(dst_pth).split(".")[2]
    set_data = ready_meals[set_number] if category == "ready" else quick_meals[set_number]
    all_pts = np.array(set_data["original_pts"]).astype(np.float32)
    dst_pts = np.array(set_data["dst_pts"]).astype(np.float32)
    dst_w, dst_h = dst_pts[2].astype(np.int)
    fr_x, fr_y, fr_w, fr_h = set_data.get("framing", [0, 0, dst_w, dst_h])

    img = cv2.imread(dst_pth)
    mtx = cv2.getPerspectiveTransform(all_pts, dst_pts)
    warped = cv2.warpPerspective(img, mtx, (dst_w, dst_h), borderValue=(0, 0, 0))
    roi = warped[fr_y:fr_y + fr_h, fr_x:fr_x + fr_w]
    cv2.imwrite(dst_pth, roi)

    anno_pts = []
    incorrect_annos = []
    for i, region in enumerate(anno_data["regions"]):
        x = max(region["x"], 0)
        y = max(region["y"], 0)
        if x == 0 and y == 0:
            incorrect_annos.append(i)
        w = region["width"]
        h = region["height"]
        anno_pts.append(np.array([[x, y], [x + w, y + h]]).astype(np.float32))

    anno_pts = np.array(anno_pts).astype(np.float32)
    transformed_pts = cv2.perspectiveTransform(anno_pts, mtx)
    transformed_pts = transformed_pts.astype(np.int32).tolist()
    for i, region in enumerate(anno_data["regions"]):
        region_pts = transformed_pts[i]
        region["x"] = max(region_pts[0][0] - fr_x, 0)
        region["y"] = max(region_pts[0][1] - fr_y, 0)
        region["width"] = region_pts[1][0] - region_pts[0][0]
        region["height"] = region_pts[1][1] - region_pts[0][1]

    for i, idx in enumerate(incorrect_annos):
        idx -= i
        del anno_data["regions"][idx]


def download_photo(entry, dst_dir, task, category):
    filename = entry.get("filename", os.path.basename(entry["publicPath"]))
    dst_pth = os.path.join(dst_dir, filename)
    entry["localPath"] = dst_pth
    wget.download(entry["publicPath"], dst_pth)

    if task == "detection":
        transform_photo_and_anno(dst_pth, category, entry)


def get_photos(src_dir):
    json_pths = list(glob.iglob(src_dir + '**/*.json', recursive=True))
    for json_pth in json_pths:
        # category: ready or quick, task: detection or classification, iteration: counter of exports
        category, _, task, iteration = os.path.basename(json_pth).replace(".json", "").split("_")
        print("Downloading data for {} meals, task: {}, iteration: {}".format(category, task, iteration))
        dst_dir = os.path.join("/tytan/raid/shelf-retail/data/orig", task, "meals", "{}_meals".format(category), iteration)
        if os.path.exists(dst_dir):
            print("Directory {} already exists - ignoring.".format(dst_dir))
            continue
        else:
            os.makedirs(dst_dir)

        with open(json_pth, "r") as f:
            json_data = json.load(f)

        # higher number of processes results in socket address-related error
        pool = ThreadPool(processes=6)

        def download(entry):
            return download_photo(entry, dst_dir, task, category)

        for _ in tqdm.tqdm(pool.imap_unordered(download, json_data)):
            pass

        with open(os.path.join(dst_dir, "annotations.json"), "w") as f:
            json.dump(json_data, f)


if __name__ == '__main__':
    get_photos(SRC_DIR)
