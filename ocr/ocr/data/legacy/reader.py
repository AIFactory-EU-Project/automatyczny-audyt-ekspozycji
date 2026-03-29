""" Legacy data reader. """
import json
import random
import re
import os
import cv2

from glob import iglob, glob

DATA_DIR = "/kolos/m2/ocr/data"


def decode_path(path):
    #                 base direct   font    box     type    id    aug       d/s    ext
    return re.match(r"(.*)/([^/]+)/([^/]+)/([^/]+)/([^/]+)/(\w\d+)_?(\d+)?_?(\w+)?\.(\w+)", path).groups()


def normalize_position(position):
    p1, p2 = position
    np1 = [min(p) for p in zip(p1, p2)]
    np2 = [max(p) for p in zip(p1, p2)]

    return [np1, np2]


def detection_samples(direction="straight*", font="*", box="*", augmentation="", paths_only=False, dates=True, serials=True):
    assert dates or serials
    main_dir = DATA_DIR
    main_path = "{main_dir}/{direction}/{font}/{box}/{augmentation}/tags/*.json".format(**locals())

    print(main_path)
    for tags_path in iglob(main_path):
        try:
            with open(tags_path) as f:
                tags = json.load(f)

            image_path = tags_path.replace("/tags/", "/front/").replace(".json", ".png")

            if paths_only:
                if not os.path.isfile(image_path):
                    raise Exception("File does not exist " + image_path)
                image = image_path
            else:
                image = cv2.imread(image_path)
                if image is None or not image.size:
                    raise Exception("Cannot read image " + image_path)

            if dates and tags.get("DATE", None):
                date_position = tags["DATE"][0]
                date_position = normalize_position(date_position)
                date_value = tags["DATE_VALUE"]
                yield image, date_position

            if serials and tags.get("SERIAL_NUMBER", None):
                serial_position = tags["SERIAL_NUMBER"][0]
                serial_position = normalize_position(serial_position)
                serial_value = tags["SERIAL_NUMBER_VALUE"]
                yield image, serial_position

        except Exception as e:
            print("ERROR:", e, tags_path)


def detection_samples_complete(direction="straight*", font="*", box="*", augmentation="", paths_only=False, shuffle=False):
    main_dir = DATA_DIR
    main_path = "{main_dir}/{direction}/{font}/{box}/{augmentation}/tags/*.json".format(**locals())

    print(main_path)
    gen = iglob(main_path)
    if shuffle:
        paths = glob(main_path)
        random.shuffle(paths)
        gen = paths

    for tags_path in gen:
        try:
            with open(tags_path) as f:
                tags = json.load(f)

            image_path = tags_path.replace("/tags/", "/front/").replace(".json", ".png")

            if paths_only:
                if not os.path.isfile(image_path):
                    raise Exception("File does not exist " + image_path)
                image = image_path
            else:
                image = cv2.imread(image_path)
                if image is None or not image.size:
                    raise Exception("Cannot read image " + image_path)

            class_names = ("DATE", "SERIAL_NUMBER")
            boxes = []
            classes = []
            for class_id, class_name in enumerate(class_names):
                if tags.get(class_name, None):
                    position = tags[class_name][0]
                    position = normalize_position(position)
                    boxes.append(position)
                    classes.append((class_id, class_name))

            yield image, boxes, classes

        except Exception as e:
            print("ERROR:", e, tags_path)


def ocr_samples(direction="straight", font="*", box="*", augmentation="", paths_only=False, dates=True, serials=True, texts=False):
    assert dates or serials or texts

    main_path = f"{DATA_DIR}/{direction}/{font}/{box}/{augmentation}/tags/*.json"

    for tags_path in iglob(main_path):
        try:
            with open(tags_path) as f:
                tags = json.load(f, encoding='utf-8')

            image_path = tags_path.replace("/tags/", "/crop/").replace(".json", ".png")

            if dates and "DATE_VALUE" in tags and tags["DATE_VALUE"]:
                date_value = tags["DATE_VALUE"]

                if not date_value: continue

                p = image_path.replace(".png", "_date.png")

                if paths_only:
                    image = p if os.path.exists(p) else None
                else:
                    image = cv2.imread(p)

                if image is not None:
                    yield image, date_value

            if serials and "SERIAL_NUMBER_VALUE" in tags and tags["SERIAL_NUMBER_VALUE"]:
                serial_value = tags["SERIAL_NUMBER_VALUE"]

                if not serial_value: continue

                p = image_path.replace(".png", "_serial.png")

                if paths_only:
                    image = p if os.path.exists(p) else None
                else:
                    image = cv2.imread(p)

                if image is not None:
                    yield image, serial_value

            if texts and "TEXT_VALUE" in tags and tags["TEXT_VALUE"]:
                text_value = tags["TEXT_VALUE"]

                if not text_value: continue

                p = image_path.replace(".png", "_text.png")

                if paths_only:
                    image = p if os.path.exists(p) else None
                else:
                    image = cv2.imread(p)

                if image is not None:
                    yield image, text_value

        except Exception as e:
            print("ERROR:", e)
            raise


def program_samples(direction="straight", font="*", box="*", augmentation=""):
    main_dir = DATA_DIR
    main_path = "{main_dir}/{direction}/{font}/{box}/{augmentation}/tags/*.json".format(**locals())
    for tags_path in iglob(main_path):
        with open(tags_path) as f:
            tags = json.load(f)

        image_path = tags_path.replace("/tags/", "/orig/").replace(".json", ".jpg")
        image = cv2.imread(image_path)

        if image is not None:
            yield image, (tags.get('DATE_VALUE', ''), tags.get('SERIAL_NUMBER_VALUE', ''), tags.get('BARCODE_VALUE', ''))


def video_samples(directory="videos"):
    main_dir = DATA_DIR
    main_path = "{}/{}/tags/*.json".format(main_dir, directory)
    for tags_path in iglob(main_path):
        with open(tags_path) as f:
            tags = json.load(f)

        video_path = tags_path.replace("/tags/", "/tester/").replace(".json", ".mkv")
        results = tags["output"]
        results.sort(key=lambda x: x["timestamp"])

        yield video_path, results


if __name__ == '__main__':
    for im, pos in detection_samples(augmentation=""):
        print("I", im.shape, pos)
        cv2.imshow("image", im)
        cv2.waitKey(1)
