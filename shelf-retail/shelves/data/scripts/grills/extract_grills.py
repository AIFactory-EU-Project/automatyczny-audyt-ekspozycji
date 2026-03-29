""" Extract grill's ROIs from original images and build a JSON with proper annotations """

import glob
import json
import os

import cv2

SRC_DIR = "/tytan/raid/shelf-retail/data/orig/detection/grills/"
DST_DIR = "/tytan/raid/shelf-retail/data/orig/detection/grills_extracted/1/"

framing = {
    "1": (769, 132, 427, 385), "2": (746, 370, 384, 329),
    "3": (744, 327, 394, 364), "4": (638, 446, 527, 491),
    "5": (479, 272, 448, 401), "6": (817, 439, 343, 268),
    "7": (882, 587, 344, 351), "8": (677, 357, 389, 371),
    "9": (826, 287, 303, 269), "10": (935, 314, 266, 293),
    "11": (900, 324, 348, 363), "12": (788, 355, 380, 341),
    "13": (873, 336, 334, 386), "14": (781, 379, 334, 249),
    "15": (881, 381, 316, 319), "16": (768, 475, 308, 339),
    "17": (701, 350, 551, 473), "18": (815, 362, 396, 358),
    "19": (692, 269, 403, 358), "20": (733, 414, 464, 404)
}


def extract(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    merged_json = {}
    json_pths = list(glob.iglob(src_dir + "**/*.json", recursive=True))
    for json_pth in json_pths:
        # ignore classes.json
        if "classes" in json_pth:
            continue

        with open(json_pth, "r") as f:
            json_data = json.load(f)

        for filekey, filedata in json_data.items():
            f_name = filedata["filename"]
            f_parts = f_name.split(".")
            # number of cameras' set
            set_number = f_parts[2] if len(f_parts) == 5 else os.path.basename(f_parts[0])
            fx, fy, fw, fh = framing[set_number]
            for _, region in filedata["regions"].items():
                x = region["shape_attributes"]["x"]
                y = region["shape_attributes"]["y"]
                region["shape_attributes"]["x"] = x - fx
                region["shape_attributes"]["y"] = y - fy

            src_img_dir = os.path.dirname(json_pth)
            img = cv2.imread(os.path.join(src_img_dir, f_name))
            extracted = img[fy:fy+fh, fx:fx+fw]
            dst_pth = os.path.join(dst_dir, f_name)
            cv2.imwrite(dst_pth, extracted)

            fsize = os.path.getsize(dst_pth)
            merged_json[f_name + str(fsize)] = filedata

    with open(os.path.join(dst_dir, "via_region_data.json"), "w") as f:
        json.dump(merged_json, f)


if __name__ == "__main__":
    extract(SRC_DIR, DST_DIR)
