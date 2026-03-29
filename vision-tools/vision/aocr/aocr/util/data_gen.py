from __future__ import print_function, unicode_literals

import random

import cv2
import numpy as np
import six
import tensorflow as tf
import sys
import logging

from PIL import Image
from six import BytesIO as IO

from vision.helpers.image_helpers import fit_to_size
from .bucketdata import BucketData


class DataGen(object):
    GO_ID = 1
    EOS_ID = 2

    def __init__(self,
                 annotation_fn,
                 buckets,
                 width,
                 height,
                 epochs,
                 charmap,
                 charsubst,
                 uppercase,
                 online_aug,
                 max_length):
        self.width = width
        self.height = height
        self.epochs = epochs

        self.charmap = ['', '', ''] + list(charmap)
        self.charsubst = charsubst
        self.uppercase = uppercase

        self.max_length = max_length

        self.online_aug = online_aug

        self.bucket_specs = buckets
        self.bucket_data = BucketData()

        dataset = tf.data.TFRecordDataset([annotation_fn])
        dataset = dataset.map(self._parse_record)
        dataset = dataset.shuffle(buffer_size=10000)
        self.dataset = dataset.repeat(self.epochs)

    def clear(self):
        self.bucket_data = BucketData()

    def gen(self, batch_size):

        dataset = self.dataset.batch(batch_size)
        iterator = dataset.make_one_shot_iterator()

        images, labels, comments = iterator.get_next()
        with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:

            while True:
                try:
                    bucket_size = 0
                    raw_images, raw_labels, raw_comments = sess.run([images, labels, comments])
                    last_bucket = None
                    for img_path, lex, comment in zip(raw_images, raw_labels, raw_comments):

                        img_path = img_path.decode("utf-8")
                        lex = lex.decode('utf-8')

                        img = cv2.imread(img_path)
                        if img is None:
                            logging.warn("{img_path} not found".format(**locals()))
                            continue

                        if self.online_aug:
                            img = self.augment(img)

                        background = cv2.mean(img)[:3]
                        img = fit_to_size(img, (self.width, self.height), 'topleft', background)

                        # cv2.imshow("test", img)
                        # cv2.waitKey()

                        for c in lex:
                            if c not in self.charmap and c not in self.charsubst:
                                logging.warn("character {} not in charmap".format(c))
                                continue

                        word = self.convert_lex(lex)

                        if len(word) > self.max_length + 2:
                            logging.warn("word too long {}/{}: {}".format(len(word)-2,self.max_length,lex))
                            continue

                        last_bucket = (img, word, lex, comment)
                        bucket_size = self.bucket_data.append(*last_bucket)
                        if bucket_size >= batch_size:
                            bucket = self.bucket_data.flush_out(self.bucket_specs, go_shift=1)
                            yield bucket

                    if bucket_size > 0 and bucket_size < batch_size and last_bucket:
                        logging.warn("bucket size {} / {}".format(bucket_size, batch_size))
                        for i in range(batch_size-bucket_size):
                            self.bucket_data.append(*last_bucket)
                        bucket = self.bucket_data.flush_out(self.bucket_specs, go_shift=1)
                        yield bucket

                except tf.errors.OutOfRangeError:
                    break

        self.clear()
        
    def convert_text(self, text):
        if self.uppercase:
            text = text.upper()

        for a, b in six.iteritems(self.charsubst):
            text = text.replace(a, b)
        
        return text
            
    def convert_lex(self, lex):
        lex = self.convert_text(lex)

        assert len(lex) < self.bucket_specs[-1][1]

        return np.array([self.GO_ID] + [self.charmap.index(char) for char in lex] + [self.EOS_ID], dtype=np.int32)

    @staticmethod
    def _parse_record(example_proto):
        features = tf.parse_single_example(
            example_proto,
            features={
                'image': tf.FixedLenFeature([], tf.string),
                'label': tf.FixedLenFeature([], tf.string),
                'comment': tf.FixedLenFeature([], tf.string, default_value=''),
            })
        return features['image'], features['label'], features['comment']

    def augment(self, image):
        if random.choice([0,1]):
            image = np.rot90(image, 2)
        return image
