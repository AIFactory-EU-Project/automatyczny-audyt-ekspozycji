import numpy as np

from vision.helpers.label_helpers import load_labels_txt_list
from vision.keras.models.networks import GeneralNeuralNetwork
from vision.keras.test import thresholds
from vision.keras.test.measures import multilabel_measures, regression_measures
from vision.keras.test.thresholds import get_ground_truth
from vision.tensorflow.gpus import tensorflow_use_gpus


def get_predictions(network, labels):
    return thresholds.get_predictions(network, labels)


def print_measures(measures):
    for k, v in sorted(measures.items()):
        print("{}: {}".format(k, v))


def print_predictions(gt, pred, labels):
    print("gt\tpred")
    for t, p, l in zip(gt, pred, labels):
        print("{}\t{}\t{}".format(t, p, l[0]))


def test_classifier(network_params, test_labels_path, threshs):
    tensorflow_use_gpus(1)

    if network_params[-1] != "sigmoid" and network_params[-1] != "softmax":
        print("Cannot calculate measures for {} last activation. Only softmax or sigmoid is allowed.".format(network_params[-1]))

    network = GeneralNeuralNetwork(*network_params)
    labels = load_labels_txt_list(test_labels_path)
    gt = get_ground_truth(labels)
    pred = get_predictions(network, labels)
    pred = np.array(pred >= threshs, dtype=np.float32)
    measures = multilabel_measures(gt, pred, threshs)

    print_measures(measures)


def test_regressor(network_params,  test_labels_path, verbose=False):
    tensorflow_use_gpus(1)

    if network_params[-1] != "linear":
        print("Cannot calculate measures for {} last activation. Only linear is allowed.".format(network_params[-1]))

    network = GeneralNeuralNetwork(*network_params)
    labels = load_labels_txt_list(test_labels_path)
    gt = get_ground_truth(labels, True)
    pred = get_predictions(network, labels)
    pred = np.round(pred)
    measures = regression_measures(gt, pred)

    if verbose:
        print_predictions(gt, pred, labels)
    print_measures(measures)
