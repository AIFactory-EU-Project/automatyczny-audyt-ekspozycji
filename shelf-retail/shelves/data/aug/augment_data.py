import glob
import json
import os
import random

import aug
import cv2
from shelves.data.aug.config import classifier
from shelves.data.aug.pipelines import ClassificationPipeline
from shelves.data.mappings.sku_mappings import sku_mapping
from vision.helpers import file_helpers as helpers


def augment_file(img_path):
    """Augment a single image <classifier.augment_repeat> times and save them to <classifier.aug_path>"""
    image = cv2.imread(img_path)
    for j in range(classifier.augment_repeat):
        image_copy = image.copy()
        sample = aug.Sample(image=image_copy)
        image_out = ClassificationPipeline().apply(sample).image
        img_name, ext = os.path.basename(img_path).rsplit(".", 1)
        new_name = img_name + ":" + str(j) + "." + ext
        phase = "val" if random.random() < classifier.val_to_train_ratio else "train"
        phase_path = os.path.join(classifier.aug_path, phase)
        if not os.path.exists(phase_path):
            os.makedirs(phase_path)
        cv2.imwrite(os.path.join(classifier.aug_path, phase, new_name), image_out)


def augment_data():
    """ Augment data using specified functions """

    img_paths = helpers.find_all_images(classifier.data_path)
    for i, img in enumerate(img_paths):
        augment_file(img)
        print("done {} out of {} images".format(i+1, len(img_paths)))

    # generate file containing pairs (image_path -> labels)
    reverted_mapping = {v[0]: v for _, v in sku_mapping.items()}
    for phase in ["train", "val"]:
        phase_path = os.path.join(classifier.aug_path, phase)
        labels = {}
        for img_path in glob.iglob(os.path.join(phase_path, "*.jpg")):
            sku_name = os.path.basename(img_path).split(":", 1)[0]
            labels[img_path] = reverted_mapping.get(sku_name, None)

        with open(os.path.join(phase_path, "labels.json"), "w") as f:
            json.dump(labels, f)


if __name__ == '__main__':
    augment_data()
