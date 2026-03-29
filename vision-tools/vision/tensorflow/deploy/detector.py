import os

import cv2 as cv
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util

from vision.imgproc.preprocess import pad_to_aspect_ratio


class TFDetector(object):

    def __init__(self, graph_path, labels_path, input_size=(300, 300), detection_threshold=0.9, gpu_memory_fraction=1.0):

        self.input_size = input_size
        self.detection_threshold = detection_threshold
        self.preprocess = None

        # Load frozen graph
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(graph_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        # Load labels
        num_classes = len(label_map_util.get_label_map_dict(labels_path))
        label_map = label_map_util.load_labelmap(labels_path)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=num_classes, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

        # Prepare tensors
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

        # Init session
        session_config = tf.ConfigProto()
        session_config.gpu_options.per_process_gpu_memory_fraction = gpu_memory_fraction
        self.session = tf.Session(graph=self.detection_graph, config=session_config)

    def predict(self, images_batch):
        images_batch = [self.resize_image(img) for img in images_batch]
        batch = np.array(images_batch)
        batch = batch[:, :, :, ::-1]
        (boxes, scores, classes, num) = self.session.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: batch})
        result = [(boxes[i], scores[i], classes[i].astype(np.int32), num[i]) for i in range(len(batch))]
        return result

    def resize_image(self, img):
        if img.shape[:2] != self.input_size:
            img = cv.resize(img, self.input_size)
        return img

    def __del__(self):
        self.session.close()


class DetectorWrapper(TFDetector):

    @classmethod
    def from_config(cls, config):
        assert os.path.exists(config.graph_path), "Invalid graph path!"
        assert os.path.exists(config.labels_path), "Invalid labels path!"
        return cls(config.graph_path, config.labels_path, config.input_size,
                   config.detection_threshold, config.gpu_memory_fraction)

    def process(self, images):
        result = []
        for index, image in enumerate(images):
            boxes_list = []
            scores_list = []
            classes_list = []
            class_names = []

            if image is not None:
                image_padded, _, (rev_y_op, rev_x_op) = pad_to_aspect_ratio(image, 1.0, norm_reverse_ops=True)[:3]
                boxes, scores, classes, num = self.predict([image_padded])[0]

                relevant_data = [(box, score, label_class) for box, score, label_class in
                                 zip(boxes.tolist(), scores.tolist(), classes.tolist()) if score > self.detection_threshold]
                if relevant_data:
                    boxes, scores, classes = zip(*relevant_data)

                    # Applying (x_min, y_min, x_max, y_max) order
                    boxes_list = [[rev_x_op(box[1]), rev_y_op(box[0]), rev_x_op(box[3]), rev_y_op(box[2])] for box in boxes]

                    # Restoring absolute coordinates
                    img_height, img_width = image.shape[:2]
                    boxes_list = [[int(box[0] * img_width), int(box[1] * img_height),
                                   int(box[2] * img_width), int(box[3] * img_height)] for box in boxes_list]

                    scores_list = list(scores)
                    classes_list = list(classes)
                    class_names = [self.category_index[i]["name"] for i in classes]

            detections = list(zip(boxes_list, scores_list, classes_list, class_names))
            result.append(detections)

        return result

