""" Convert data structure from former one kept on /kolos/storage/ocr/m2/data/ to the new one used by tagger. """
import json
import os
import glob
import cv2
import numpy as np

from enum import Enum

from vision.helpers import file_helpers

SRC = "/tytan/raid/neuca/data/orig/former_data/"
DST = "/tytan/raid/neuca/data/orig/former_data/_former"


class Status(Enum):
    # consistent with tagger statuses
    STATUS_INACTIVE = 0
    STATUS_DONE = 2


def get_correct_upper_left_coords(x1, y1, x2, y2):
    """ Get pair of (upper_left, bottom_right) coordinates

    :param x1: A x-coordinate of supposed upper left corner.
    :param y1: A y-coordinate of supposed upper left corner.
    :param x2: A x-coordinate of supposed bottom right corner.
    :param y2: A y-coordinate of supposed bottom right corner.
    """
    x, y = x1, y1
    xx, yy = x2, y2
    if y2 < y1 and x2 > x1:
        # (x1, y1) is bottom left corner
        y = y2
        yy = y1
    elif y2 < y1 and x2 < x1:
        # (x1, y1) is bottom right corner
        x = x2
        y = y2
        xx = x1
        yy = y1
    elif x2 < x1:
        # (x1, y1) is upper right corner
        x = x2
        xx = x1

    return int(x), int(y), int(xx), int(yy)


def build_date_serial_annos(box_data, annos, data_type, im_height, im_width, crop_pth):
    """
    Convert annotations defining areas of date and serial number to the new format.

    :param box_data: A json object containing box's data.
    :param annos: A list of annotations defining bounding box of date or serial number.
    :param data_type: A string specifying whether area is date or serial number.
    :param im_height: A height of the box's image.
    :param im_width: A width of the box's image.
    :param crop_pth: A path to the image containing area of date or serial number.
    """
    box_data["{}LabelArea".format(data_type)] = None
    box_data["{}LabelStatus".format(data_type)] = Status.STATUS_INACTIVE.value
    box_data["{}LabelPhoto".format(data_type)] = ""
    box_data["{}DataArea".format(data_type)] = None
    box_data["{}DataStatus".format(data_type)] = Status.STATUS_INACTIVE.value
    box_data["{}DataPhoto".format(data_type)] = ""

    if annos.size == 0 or cv2.imread(crop_pth) is None:
        return

    counter = 0
    for anno in annos:
        anno[:, 0] *= im_width
        anno[:, 1] *= im_height
        anno = anno.astype(np.int)
        x1, y1 = anno[0][0], anno[0][1]
        x2, y2 = anno[1][0], anno[1][1]
        if (x1, y2) == (x2, y2):
            continue  # some invalid data (point instead of rect)

        # there should be only ONE valid data
        assert counter == 0
        counter += 1
        x, y, xx, yy = get_correct_upper_left_coords(x1, y1, x2, y2)
        box_data["{}DataArea".format(data_type)] = {"x": x, "y": y, "width": xx - x, "height": yy - y,
                                                    "rotate": 0, "scaleX": 1, "scaleY": 1}
        box_data["{}DataPhoto".format(data_type)] = crop_pth
        box_data["{}DataStatus".format(data_type)] = Status.STATUS_DONE.value


def build_from_former(src, dst):
    """ Build data from the old format to the new one (used by tagger).

    :param src: A source directory where data is kept in the old format.
    :param dst: A destination directory where data is kept in the new format.
    """
    if os.path.exists(dst):
        raise Exception("Data directory already exists - omitting!")

    os.makedirs(dst)
    all_boxes = []
    i = 0
    # take all original samples (667)
    for json_pth in glob.iglob(f"{src}/straight*/*/*//tags/*.json"):
        with open(json_pth, "r") as f:
            json_data = json.load(f)

        box_data = {}

        json_dir = os.path.dirname(json_pth)
        front_dir = json_dir.replace("tags", "front")
        front_pths = file_helpers.find_all_images(front_dir)
        # exactly one front image is expected
        assert len(front_pths) == 1
        front_pth = front_pths[0]
        box_data["boxPhoto"] = front_pth

        orig_dir = json_dir.replace("tags", "orig")
        orig_pths = file_helpers.find_all_images(orig_dir)
        if not orig_pths:
            # if there is no original image, use the front one instead
            orig_pth = front_pth
        else:
            # exactly one original image is expected
            assert len(orig_pths) == 1
            orig_pth = orig_pths[0]

        orig_name = os.path.basename(orig_pth)
        box_data["originalPhotoName"] = orig_name
        box_data["originalPhoto"] = orig_pth
        box_data["boxArea"] = None

        local_name, ext = orig_name.split(".")
        local_name = local_name + "_{}.".format(str(i)) + ext
        os.symlink(orig_pth, os.path.join(dst, local_name))
        box_data["localPath"] = os.path.join(dst, local_name)

        crop_dir = json_dir.replace("tags", "crop")
        crop_pths = file_helpers.find_all_images(crop_dir)
        crop_pths.sort()
        date_pth, serial_pth = "", ""
        for pth in crop_pths:
            if "date" in pth:
                date_pth = pth
            elif "serial" in pth:
                serial_pth = pth

        box_img = cv2.imread(front_pth)

        anno = np.array(json_data["SERIAL_NUMBER"])
        build_date_serial_annos(box_data, anno, "series", *box_img.shape[:2], serial_pth)

        anno = np.array(json_data["DATE"])
        build_date_serial_annos(box_data, anno, "date", *box_img.shape[:2], date_pth)

        series_txt = json_data["SERIAL_NUMBER_VALUE"]
        box_data["seriesText"] = series_txt
        box_data["seriesTextStatus"] = Status.STATUS_DONE.value if series_txt else Status.STATUS_INACTIVE.value

        date_txt = json_data["DATE_VALUE"]
        box_data["dateText"] = date_txt
        box_data["dateTextStatus"] = Status.STATUS_DONE.value if date_txt else Status.STATUS_INACTIVE.value

        all_boxes.append(box_data)
        i += 1

    with open(os.path.join(dst, "annotations.json"), "w") as f:
        json.dump(all_boxes, f)


if __name__ == '__main__':
    build_from_former(SRC, DST)
