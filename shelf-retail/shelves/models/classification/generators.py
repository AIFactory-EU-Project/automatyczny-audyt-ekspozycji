import json
import random
import cv2
import numpy as np

from collections import defaultdict

from keras.utils import Sequence
from vision.helpers import label_helpers
from vision.imgproc import preprocess


class MealsClassifierBatchGenerator:
    def __init__(self, data_file, input_size, batch_size, classes_no, multilabel=False, use_unknown_class=True, **kwargs):
        self.data = None
        self.aug_data = None
        self.classes = None
        self.aug_classes = None
        self.classes_no = classes_no
        self.multilabel = multilabel
        self.grayscale = kwargs.get("grayscale", False)
        self.pad_image = kwargs.get("pad_image", False)
        self.batch_size = batch_size
        self.input_size = input_size
        self.use_unknown_class = use_unknown_class

        self.mapping_path = kwargs.get("mapping_path", "")
        self.load_data(data_file)

    def load_data(self, data_file):
        with open(self.mapping_path, "r") as f:
            mapping = json.load(f)

        org_data = defaultdict(list)  # id -> (path, [labels])
        aug_data = defaultdict(list)
        for data_id, data_path in enumerate(sorted(data_file)):
            print("DEBUG Loading meals train data from:", data_path)

            if "aug" in data_path:
                data = aug_data
            else:
                data = org_data

            data_id = str(data_id) + ":"
            paths = label_helpers.load_labels_json_dict(data_path)
            for path, labels in paths.items():
                labels = set(labels)
                is_unknown = all(l is None for l in labels)
                is_specific = any(len(l.split(" ")) != 1 for l in labels if l is not None)
                assert len(labels) <= 2

                if not self.use_unknown_class and is_unknown:
                    labels.difference_update([0])

                labels = list(labels)
                mapped_labels = [mapping.get(l, 0) for l in labels]

                if is_unknown:
                    data[data_id + "unknown"].append((path, mapped_labels))
                else:
                    for label, mapped_label in list(zip(labels, mapped_labels)):
                        # don't add to general classes if is specific class
                        if len(label.split(" ")) == 1 and is_specific:
                            continue
                        data[data_id + str(mapped_label)].append((path, mapped_labels))

        self.classes = list(org_data.keys())
        self.aug_classes = list(aug_data.keys())
        self.data = org_data
        self.aug_data = aug_data

        print("DEBUG Train data loaded. Classes:")
        for c, items in sorted(self.data.items()):
            print("- {}:\t{}".format(c, len(items)))

    def next_batch(self):
        from keras.applications import imagenet_utils

        x_buffer = []
        y_buffer = []

        while len(x_buffer) < self.batch_size:
            try:
                path, label_ids = self.random_sample()
                label_ids = [int(i) for i in label_ids]

                img = cv2.imread(path)
                if img is None or not img.size:
                    raise Exception("Cannot read image: {}".format(path))

                if self.pad_image:
                    img, _, _ = preprocess.pad_to_aspect_ratio(img, 1.0)

                inter = cv2.INTER_LINEAR
                if max(img.shape[:2]) > max(self.input_size[:2]):
                    inter = cv2.INTER_AREA

                img = cv2.resize(img, self.input_size[:2], interpolation=inter)

                if self.grayscale:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

                img = imagenet_utils.preprocess_input(img, data_format="channels_last", mode='tf')

                labels = np.zeros(self.classes_no, np.float32)
                labels[label_ids] = 1

                x_buffer.append(img)
                y_buffer.append(labels)

            except Exception as e:
                print("WARN Error during training batch read:", e)

        return x_buffer, y_buffer

    def random_sample(self):
        if random.random() < .67:
            classid = random.choice(self.classes)
            return random.choice(self.data[classid])
        else:
            classid = random.choice(self.aug_classes)
            return random.choice(self.aug_data[classid])


class MealsClassifierTestDataGenerator(Sequence):
    def __init__(self, batch_size, input_size, data_file, classes_no, multilabel=False, use_unknown_class=True, **kwargs):
        self.batch_size = batch_size
        self.input_size = input_size
        self.classes_no = classes_no
        self.multilabel = multilabel
        self.grayscale = kwargs.get("grayscale", False)
        self.pad_image = kwargs.get("pad_image", False)
        self.data = []
        self.use_unknown_class = use_unknown_class
        self.mapping_path = kwargs.get("mapping_path", "")

        if data_file:
            self.load_data(data_file)

        self.index = 0

    def load_data(self, data_file):
        with open(self.mapping_path, "r") as f:
            mapping = json.load(f)

        print("DEBUG Loading meals test/val data from:", data_file)
        paths = label_helpers.load_labels_json_dict(data_file)
        for path, labels in paths.items():
            labels = set(labels)
            is_unknown = all(l is None for l in labels)
            assert len(labels) <= 2

            if not self.use_unknown_class and is_unknown:
                labels.difference_update([""])

            labels = list(labels)
            labels = [mapping.get(l, 0) for l in labels]
            self.data.append((path, labels))

        print("DEBUG Data loaded.")

    def __len__(self):
        return int(np.floor(len(self.data) / self.batch_size))

    def __getitem__(self, index):
        from keras.applications import imagenet_utils

        x_buffer = []
        y_buffer = []
        for i in range(self.batch_size):
            path, label_ids = self.data[self.index]

            img = cv2.imread(path)
            if img is None:
                raise Exception("Cannot read image: {}".format(path))

            if self.pad_image:
                img, _, _ = preprocess.pad_to_aspect_ratio(img, 1.0)

            inter = cv2.INTER_LINEAR
            if max(img.shape[:2]) > max(self.input_size[:2]):
                inter = cv2.INTER_AREA

            img = cv2.resize(img, self.input_size[:2], interpolation=inter)

            if self.grayscale:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            labels = np.zeros(self.classes_no, np.float32)
            labels[label_ids] = 1

            img = imagenet_utils.preprocess_input(img, data_format="channels_last", mode='tf')

            x_buffer.append(img)
            y_buffer.append(labels)

            self.index += 1
            if self.index >= len(self.data):
                self.index = 0
                break

        return np.array(x_buffer), np.array(y_buffer)


class MealsClassifierValDataGenerator(MealsClassifierTestDataGenerator):
    def __init__(self, batch_size, input_size, data_file, classes_no, multilabel=False, max_validation_size=None,
                 **kwargs):
        super().__init__(batch_size, input_size, data_file, classes_no, multilabel, **kwargs)

        print("INFO Validation data length:", len(self.data))

        if max_validation_size and len(self.data) > max_validation_size:
            print("WARN Clipping validation set from {} to {} samples.".format(len(self.data), max_validation_size))
            random.seed(0)
            self.data = random.sample(self.data, max_validation_size)
