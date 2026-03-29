from __future__ import print_function

import sys

import six
import tensorflow as tf
import logging
import re

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


python3 = sys.version_info >= (3,0)


def prepare_tf_example(img_path, label, substitutions, force_uppercase, save_filename):
    if force_uppercase:
        label = label.upper()

    for a, b in six.iteritems(substitutions):
        label = label.replace(a, b)

    label = re.sub(r"\s+", " ", label)
    feature = {}
    if python3:
        img_path = bytes(img_path, 'utf-8')
        label = bytes(label, 'utf-8')
    else:
        img_path = img_path.encode("utf-8")
        label = label.encode("utf-8")

    feature['image'] = _bytes_feature(img_path)
    feature['label'] = _bytes_feature(label)
    if save_filename:
        feature['comment'] = _bytes_feature(img_path)

    example = tf.train.Example(features=tf.train.Features(feature=feature))
    return example.SerializeToString()


def generate_iter(data, output_path, log_step=5000, force_uppercase=True, save_filename=False, substitutions=None):
    """data = (path, label)"""

    logging.info('Output file: %s', output_path)
    writer = tf.python_io.TFRecordWriter(output_path)

    substitutions = substitutions or {}
    idx = None
    for idx, (img_path, label) in enumerate(data):
        try:
            if not img_path or not label:
                logging.warn("Empty path/label data")
                continue

            example = prepare_tf_example(img_path, label, substitutions, force_uppercase, save_filename)
            writer.write(example)
        except TypeError as e:
            logging.warn("Error during data generation: {}".format(e))

        if idx % log_step == 0:
            logging.info('Processed %s pairs.', idx + 1)

    if idx is None:
        logging.error('Empty dataset!')
        raise Exception("Empty dataset!")
    else:
        logging.info('Dataset is ready: %i pairs.', idx + 1)

    writer.close()


def generate(annotations_path, *args, **kwargs):
    logging.info('Building a dataset from %s.', annotations_path)

    with open(annotations_path, 'r') as f:

        def data():
            for idx, line in enumerate(f):
                line = line.rstrip('\n')
                try:
                    (img_path, label) = line.split('\t', 1)
                except ValueError:
                    logging.error('missing filename or label, ignoring line %i: %s', idx + 1, line)
                    continue

        generate_iter(data(), *args, **kwargs)
