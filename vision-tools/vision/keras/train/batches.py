from abc import ABC, abstractmethod
from distutils.util import strtobool

import cv2
import numpy as np

from vision.helpers import label_helpers as helpers
from vision.imgproc import preprocess


class BatchGenerator(ABC):

    def __init__(self, data_file, input_size, batch_size, **kwargs):
        self.data = helpers.load_labels_txt_list(data_file)
        self.batch_size = batch_size
        self.input_size = input_size

    @abstractmethod
    def next_batch(self):
        pass


class ImageBatchGenerator(BatchGenerator):

    def __init__(self, data_file, input_size, batch_size, **kwargs):
        super().__init__(data_file, input_size, batch_size, **kwargs)
        self.index = 0
        self.grayscale = kwargs.get("grayscale", False)
        self.pad_image = kwargs.get("pad_image", False)

    def get_label(self, path):
        return None

    def next_batch(self):
        from keras.applications import imagenet_utils
        
        x_buffer = []
        y_buffer = []
        for i in range(self.batch_size):
            path = self.data[self.index][0]
            img = cv2.imread(path)

            if self.pad_image:
                img, _, _ = preprocess.pad_to_aspect_ratio(img, 1.0)

            inter = cv2.INTER_LINEAR
            if max(img.shape[:2]) > max(self.input_size[:2]):
                inter = cv2.INTER_AREA

            img = cv2.resize(img, self.input_size[:2], interpolation=inter)

            if self.grayscale:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            label = self.get_label(self.data[self.index][1])

            self.index += 1
            if self.index >= len(self.data):
                self.index = 0

            img = imagenet_utils.preprocess_input(img, mode='tf')
            
            x_buffer.append(img)
            y_buffer.append(label)

        return x_buffer, y_buffer


class ClassifierBatchGenerator(ImageBatchGenerator):

    def __init__(self, data_file, input_size, batch_size, **kwargs):
        super().__init__(data_file, input_size, batch_size, **kwargs)
        self.classes_no = max([v[1] for v in self.data]) + 1

    def get_label(self, val):
        from keras.utils import np_utils

        index = int(val)

        if index < 0:
            return np.full(self.classes_no, 0.0, dtype=np.float32)

        return np_utils.to_categorical(index, self.classes_no)


class BinaryClassifierBatchGenerator(ImageBatchGenerator):

    def __init__(self, data_file, input_size, batch_size, **kwargs):
        super().__init__(data_file, input_size, batch_size, **kwargs)

    def get_label(self, val):
        if isinstance(val, str):
            return int(strtobool(val))

        return int(val)


class RegressionBatchGenerator(ImageBatchGenerator):

    def __init__(self, data_file, input_size, batch_size, **kwargs):
        super().__init__(data_file, input_size, batch_size, **kwargs)

    def get_label(self, val):
        return int(val)


class PerspectiveRegressionBatchGenerator(ImageBatchGenerator):

    def __init__(self, data_file, input_size, batch_size, **kwargs):
        super().__init__(data_file, input_size, batch_size, **kwargs)

    def get_label(self, val):
        return val
