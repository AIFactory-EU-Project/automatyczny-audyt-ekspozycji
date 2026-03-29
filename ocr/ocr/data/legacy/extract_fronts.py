""" Extract fronts of the boxes. """

import cv2
import os

from glob import iglob
from multiprocessing import Pool

from ocr.data.legacy import extract_front
from vision.helpers.file_helpers import makedirs


DATA_DIR = "/kolos/m2/ocr/data"


def extract(path):
    print("INFO: processing", path)

    bg_path = path.replace("/orig/", "/bg/")
    top_path = path.replace("/orig/", "/top/").replace(".jpg", ".png")
    front_path = path.replace("/orig/", "/front/").replace(".jpg", ".png")

    bg = cv2.imread(bg_path)
    image = cv2.imread(path)

    extracted = extract_front.process(extract_front.Data(bg), extract_front.Data(image))

    top = extracted["o1"].value
    front = extracted["o2"].value

    makedirs(os.path.dirname(top_path))
    makedirs(os.path.dirname(front_path))

    cv2.imwrite(top_path, top, (cv2.IMWRITE_PNG_COMPRESSION, 9))
    cv2.imwrite(front_path, front, (cv2.IMWRITE_PNG_COMPRESSION, 9))


def extract_all():
    paths = iglob(DATA_DIR + "/straight[123]/*/*/orig/*")
    pool = Pool()
    pool.map(extract, paths)


if __name__ == '__main__':
    extract_all()

