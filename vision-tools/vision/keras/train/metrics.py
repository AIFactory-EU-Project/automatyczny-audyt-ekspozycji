import sys

import numpy as np
import tensorflow as tf
from keras import backend as K


def whole_accuracy(y_true, y_pred):
    return K.mean(K.all(K.equal(y_true, K.round(y_pred)), axis=1), axis=-1)


def f1_score(y_true, y_pred):
    def recall(y_true, y_pred):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)), axis=0)
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)), axis=0)
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision(y_true, y_pred):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)), axis=0)
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)), axis=0)
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


def f1_score_spec(y_true, y_pred):
    def sensitivity(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)), axis=0)
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)), axis=0)
        sens = true_positives / (possible_positives + K.epsilon())
        return sens

    def specificity(y_true, y_pred):
        true_negatives = K.sum(K.round(K.clip((1 - y_true) * (1 - y_pred), 0, 1)), axis=0)
        possible_negatives = K.sum(1 - K.round(K.clip(y_true, 0, 1)), axis=0)
        spec = true_negatives / (possible_negatives + K.epsilon())
        return spec

    y_pred = tf.convert_to_tensor(y_pred, np.float32)
    y_true = tf.convert_to_tensor(y_true, np.float32)
    spec = specificity(y_true, y_pred)
    sens = sensitivity(y_true, y_pred)
    return K.mean(2 * ((spec*sens)/(spec+sens+K.epsilon())))


def get(identifier):
    this_mod = sys.modules[__name__]
    return getattr(this_mod, identifier, None)
