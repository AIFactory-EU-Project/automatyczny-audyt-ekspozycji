import sys

from keras import backend as K

from vision.keras.train.metrics import f1_score


def binary_crossentropy_with_threshold(y_true, y_pred):
    return K.mean(K.binary_crossentropy(y_true, y_pred), axis=-1) + (1 - K.mean(K.all(K.equal(y_true, K.round(y_pred)), axis=1), axis=-1))


def binary_crossentropy_with_threshold_and_f1score(y_true, y_pred):
    return binary_crossentropy_with_threshold(y_true, y_pred) + 1 - f1_score(y_true, y_pred)


def binary_crossentropy_with_last_hard(y_true, y_pred):
    mul = K.ones_like(y_true) - (y_true[...,-1] * 0.9)
    mul[...,-1] = 1
    return K.binary_crossentropy(y_true*mul, y_pred*mul)


def get(identifier):
    this_mod = sys.modules[__name__]
    return getattr(this_mod, identifier, None)
