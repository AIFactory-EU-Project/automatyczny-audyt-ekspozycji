import cv2
import numpy as np

from vision.helpers.label_helpers import load_labels_txt_list
from vision.helpers.showing_progress import showing_progress
from vision.keras.models.networks import GeneralNeuralNetwork
from vision.keras.test.measures import multilabel_measures
from vision.tensorflow.gpus import tensorflow_use_gpus


def chunks(l, chunksize):
    n = int(np.ceil(len(l) / chunksize))
    return np.array_split(l, n)


def get_ground_truth(labels, one_output=False):
    from keras.utils import np_utils

    classes_no = max([int(l[1]) for l in labels]) + 1
    if one_output or classes_no == 2:
        return np.array([[int(label)] for _, label in labels], dtype=np.float32)

    return np.array([np_utils.to_categorical(int(label), classes_no) if label >= 0 else np.full(classes_no, 0) for _, label in labels], dtype=np.float32)


def get_predictions(network, labels, batchsize=32):
    preds = []
    batches = chunks(labels, batchsize)

    for batch in showing_progress(batches):
        imgs = [cv2.imread(path) for path, _ in batch]
        result = network.predict(imgs)
        preds.extend(result)

    return np.array(preds)


def find_thresholds(gt, pred, measure_to_max):
    thresh = np.arange(0.0, 1.0, 0.001)
    results = np.empty((thresh.shape[0], gt.shape[1]))
    for i, t in enumerate(thresh):
        results[i, :] = multilabel_measures(gt, pred, threshold=t, mean_result=False)[measure_to_max]

    # take value from the middle, not first or last occurrence
    first = np.argmax(results, axis=0)
    last = thresh.shape[0] - np.argmax(results[::-1] - 1, axis=0)
    return thresh[(first + last) // 2]


def determine_thresholds(network_params, val_labels_path, measure_to_max="fscore"):
    tensorflow_use_gpus(1)

    network = GeneralNeuralNetwork(*network_params)
    labels = load_labels_txt_list(val_labels_path)
    gt = get_ground_truth(labels)
    pred = get_predictions(network, labels)

    thresholds = find_thresholds(gt, pred, measure_to_max)
    print("Thresholds:")
    print(", ".join([str(round(thresh, 3)) for thresh in thresholds]))
