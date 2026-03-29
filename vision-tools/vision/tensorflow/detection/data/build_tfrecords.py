"""
Script for building TFRecords with data for object detection

Generated TFRecords are saved in {tfrecords_dir}/{set_name}/
"""

import os
import cv2 as cv
import tensorflow as tf

from object_detection.utils import dataset_util
from vision.tensorflow.detection.data.data_reader import DataReader


class TFRecordBuilder:
    def __init__(self, reader=DataReader()):
        self.reader = reader

    def build_tfrecord(self, generator, output_path):
        parent_dir = os.path.dirname(output_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        writer = tf.python_io.TFRecordWriter(output_path)
        for file_path, image, bounding_boxes in generator:
            tf_example = self.create_tf_example(file_path, image, bounding_boxes)
            writer.write(tf_example.SerializeToString())
        writer.close()

    def build_detection_samples_from_dataset(self, dataset_directory):
        assert os.path.isdir(dataset_directory), "Please set correct dataset directory before running script"

        gen_train = self.reader.get_normalized_detection_samples(os.path.join(dataset_directory, "train"))
        output_path_train = os.path.join(dataset_directory, "train", "tfrecords", "detection_train.record")
        self.build_tfrecord(gen_train, output_path_train)

        gen_val = self.reader.get_normalized_detection_samples(os.path.join(dataset_directory, "val"))
        output_path_val = os.path.join(dataset_directory, "val", "tfrecords", "detection_val.record")
        self.build_tfrecord(gen_val, output_path_val)

        gen_test = self.reader.get_normalized_detection_samples(os.path.join(dataset_directory, "test"))
        output_path_test = os.path.join(dataset_directory, "test", "tfrecords", "detection_test.record")
        self.build_tfrecord(gen_test, output_path_test)

    @staticmethod
    def create_tf_example(file_path, image, bounding_boxes):
        image_height, image_width = image.shape[:2]
        filename = file_path.encode()
        encoded_image_data = cv.imencode(".jpeg", image)[1].tostring()
        image_format = b"jpeg"

        x_mins = [box[0][0] for box in bounding_boxes]
        x_maxs = [box[1][0] for box in bounding_boxes]
        y_mins = [box[0][1] for box in bounding_boxes]
        y_maxs = [box[1][1] for box in bounding_boxes]

        classes = [box[2] for box in bounding_boxes]

        tf_example = tf.train.Example(features=tf.train.Features(feature={
            "image/height": dataset_util.int64_feature(image_height),
            "image/width": dataset_util.int64_feature(image_width),
            "image/filename": dataset_util.bytes_feature(filename),
            "image/source_id": dataset_util.bytes_feature(filename),
            "image/encoded": dataset_util.bytes_feature(encoded_image_data),
            "image/format": dataset_util.bytes_feature(image_format),
            "image/object/bbox/xmin": dataset_util.float_list_feature(x_mins),
            "image/object/bbox/xmax": dataset_util.float_list_feature(x_maxs),
            "image/object/bbox/ymin": dataset_util.float_list_feature(y_mins),
            "image/object/bbox/ymax": dataset_util.float_list_feature(y_maxs),
            "image/object/class/label": dataset_util.int64_list_feature(classes),
        }))
        return tf_example


def main(_):
    dataset_directory = "/tytan/raid/take-task/pylons/datasets/original"
    builder = TFRecordBuilder()
    builder.build_detection_samples_from_dataset(dataset_directory)


if __name__ == "__main__":
    tf.app.run()
