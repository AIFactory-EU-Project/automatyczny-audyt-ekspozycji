"""
Functions for reading and manipulating data for object detection
Data kept in two dirs: images and labels
"""

import glob
import json
import os

import cv2 as cv
import numpy as np

from vision.helpers import file_helpers


class DataReader:
    def __init__(self):
        self.class_map = self.create_class_map()

    def create_class_map(self):
        class_map = {"box": 1}
        return class_map

    @staticmethod
    def get_label_map_item(item_id, name):
        return "item {{\n  id: {0}\n  name: '{1}'\n}}\n".format(item_id, name)

    def get_detection_label_map_data(self):
        label_map_data = ""
        for key, value in sorted(self.class_map.items(), key=lambda i: i[1]):
            label_map_data = "".join([label_map_data,
                                      self.get_label_map_item(value, key)])
        return label_map_data

    @staticmethod
    def get_image_and_annotation(set_dir):
        images_paths_list = file_helpers.find_all_images(set_dir)

        for image_path in images_paths_list:
            image = cv.imread(image_path)

            name = os.path.basename(image_path).rpartition(".")[0]
            annotation_file_path = os.path.join(set_dir, "labels", "".join([name, ".json"]))
            with open(annotation_file_path) as annotation_file:
                annotation_data = json.load(annotation_file)

            yield image_path, image, annotation_data

    @staticmethod
    def normalize_point(point, width, height):
        norm_width = min(max(1.0 * point[0] / width, 0.0), 1.0)
        norm_height = min(max(1.0 * point[1] / height, 0.0), 1.0)
        return norm_width, norm_height

    @staticmethod
    def get_bounding_rect_points(coordinates):
        x, y, box_width, box_height = cv.boundingRect(np.array(coordinates))
        point_min = (x, y)
        point_max = (x + box_width, y + box_height)
        return point_min, point_max

    @staticmethod
    def get_normalized_box(coordinates, image_shape, pre_norm_operations=None, post_norm_operations=None):
        point_min, point_max = DataReader.get_bounding_rect_points(coordinates)

        if pre_norm_operations is not None:
            point_min = (pre_norm_operations[0](point_min[0]), pre_norm_operations[1](point_min[1]))
            point_max = (pre_norm_operations[0](point_max[0]), pre_norm_operations[1](point_max[1]))

        point_min_norm = DataReader.normalize_point(point_min, image_shape[1], image_shape[0])
        point_max_norm = DataReader.normalize_point(point_max, image_shape[1], image_shape[0])

        if post_norm_operations is not None:
            point_min_norm = (post_norm_operations[0](point_min_norm[0]), post_norm_operations[1](point_min_norm[1]))
            point_max_norm = (post_norm_operations[0](point_max_norm[0]), post_norm_operations[1](point_max_norm[1]))

        return point_min_norm, point_max_norm

    def get_normalized_detection_samples(self, set_dir):
        pass


def main():
    data_directory = "/tytan/raid/drugs-counter/datasets/boxes/all_faces_augmented_v2"
    reader = DataReader()

    data = reader.get_detection_label_map_data()
    data_path = os.path.join(data_directory, "detection_label_map.pbtxt")
    with open(data_path, "w") as data_file:
        data_file.write(data)


if __name__ == "__main__":
    main()
