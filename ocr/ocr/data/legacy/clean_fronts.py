""" Clean fronts of the boxes. """
import json
import os
import cv2
import numpy as np

from glob import iglob
from multiprocessing import Pool

from vision.helpers.file_helpers import makedirs


DATA_DIR = "/kolos/m2/ocr/data"


def clean(path):
    print("INFO: processing", path)
    tags_path = path.replace("/front/", "/tags/").replace(".png", ".json")
    out_path = path.replace("/front/", "/clean/")

    image = cv2.imread(path)

    if not os.path.exists(tags_path):
        return image, None, None

    if os.path.exists(out_path):
        return image, None, cv2.imread(out_path)

    meta = json.load(open(tags_path))

    rects = meta["SERIAL_NUMBER"] + meta["DATE"]

    if not rects:
        return image, None, None

    mask = image[..., 0]*0

    for rect in rects:
        rect = np.array(rect)
        rect *= mask.shape[::-1]
        (x1, y1), (x2, y2) = rect.astype(int)
        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

    mask = cv2.dilate(mask, cv2.getStructuringElement(2, (5, 5)))

    cleaned = cv2.inpaint(image, mask, 41, 1)

    print("INFO: saving", out_path)
    makedirs(os.path.dirname(out_path))
    cv2.imwrite(out_path, cleaned, (cv2.IMWRITE_PNG_COMPRESSION, 9))

    return image, mask, clean


def clean_all():
    files = iglob(DATA_DIR + "/straight[123]/*/*/front/*.png")
    pool = Pool()
    pool.map(clean, files)


if __name__ == '__main__':
    clean_all()
