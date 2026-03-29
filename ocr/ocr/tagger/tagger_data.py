""" Download annotated data"""

import glob
import json
import os
import wget
import tqdm

from multiprocessing.pool import ThreadPool

SRC_DIR = "/tytan/raid/neuca/data/orig/tagger_exports"


def download_photo(entry, dst_dir, iteration):
    filename = entry["originalPhotoName"]
    dst_pth = os.path.join(dst_dir, filename)

    # tagged photos already should be in neuca_data directory
    data_dir = "/tytan/raid/neuca/data/orig/neuca_data/{}".format(iteration)
    data_img_pths = list(glob.iglob(data_dir + '**/*.jpg'))
    for img_pth in data_img_pths:
        if os.path.basename(img_pth) == filename:
            os.symlink(img_pth, dst_pth)
            break

    if not os.path.exists(dst_pth):
        wget.download(entry["originalPhoto"], dst_pth)

    entry["localPath"] = dst_pth


def get_photos(src_dir):
    json_pths = list(glob.iglob(src_dir + '**/*.json'))
    for json_pth in json_pths:
        # iteration: counter of exports; 0 indicates special export for legacy data tagged via new tagger.
        iteration = os.path.basename(json_pth).split(".")[0]
        print("Downloading data, iteration: {}".format(iteration))
        dst_dir = os.path.join("/tytan/raid/neuca/data/orig/tagger_data", iteration)
        if os.path.exists(dst_dir):
            print("Directory {} already exists - ignoring.".format(dst_dir))
            continue
        else:
            os.makedirs(dst_dir)

        with open(json_pth, "r") as f:
            json_data = json.load(f)

        # higher number of processes results in socket address-related error
        pool = ThreadPool(processes=1)

        def download(entry):
            return download_photo(entry, dst_dir, iteration)

        for _ in tqdm.tqdm(pool.imap_unordered(download, json_data)):
            pass

        with open(os.path.join(dst_dir, "annotations.json"), "w") as f:
            json.dump(json_data, f)


if __name__ == '__main__':
    get_photos(SRC_DIR)
