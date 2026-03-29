import os
import cv2
import numpy as np

from keras import backend as K, Model
from keras.applications import imagenet_utils
from keras.layers import Activation, Dense
from keras.utils import get_custom_objects


CKPT_PTH = os.path.join(os.path.dirname(__file__), "../../models/bin/meals_cls.hdf5")


_model = None


class ReLU_Max(Activation):
    def __init__(self, activation, **kwargs):
        super(ReLU_Max, self).__init__(activation, **kwargs)
        self.__name__ = 'ReLU_with_max_value'


def relu_with_max_value(x, alpha=0.0, max_value=2.0):
    return K.relu(x, alpha, max_value) - 1


def resnext(class_number, activation="sigmoid"):
    import keras
    from keras_applications.resnext import ResNeXt101

    model = ResNeXt101(include_top=False, weights=None, input_shape=(224, 224, 3), pooling="avg",
                       backend=keras.backend, layers=keras.layers, models=keras.models, utils=keras.utils)
    current_output = model.layers[-1].output
    current_layer = Dense(class_number, activation=activation)
    current_layer.name = "dense_{}".format(activation)
    current_output = current_layer(current_output)

    return Model(inputs=[model.input], outputs=[current_output])


def set_memory_usage(fraction):
     # set_memory_usage
     import tensorflow as tf
     from keras.backend.tensorflow_backend import set_session
     config = tf.ConfigProto()
     config.gpu_options.per_process_gpu_memory_fraction = fraction
     set_session(tf.Session(config=config))


def get_classifier_model(name, class_number, memory_fraction=None):
    global _model
    if _model is None:
        if memory_fraction is not None:
            set_memory_usage(memory_fraction)
        get_custom_objects().update({'relu_with_max_value': ReLU_Max(relu_with_max_value)})
        model = resnext(class_number)
        model.name = name
        model.load_weights(CKPT_PTH)
        _model = model
    return _model


def preprocess_image(img):
    img, _, _ = pad_to_aspect_ratio(img, 1.0)
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA if max(img.shape) > 224 else cv2.INTER_LINEAR)
    img = imagenet_utils.preprocess_input(img.astype(np.float32), mode='tf')
    return img


def pad_to_aspect_ratio(img, aspect_ratio, pad_value=(127, 127, 127), norm_offset_ops=True, norm_reverse_ops=False):
    width = img.shape[1]
    height = img.shape[0]
    missing_width = 0
    missing_height = 0

    if 1.0 * width / height < aspect_ratio:
        missing_width = int(height * aspect_ratio) - width
    elif 1.0 * width / height > aspect_ratio:
        missing_height = int(width / aspect_ratio) - height

    offset_h = int(missing_height / 2)
    offset_w = int(missing_width / 2)

    padded = cv2.copyMakeBorder(img,  offset_h, offset_h, offset_w, offset_w, 0, value=pad_value)

    def offset_y_op(y):
        return y + offset_h

    def offset_x_op(x):
        return x + offset_w

    def norm_offset_y_op(y):
        return (y * height + offset_h) / (height + 2 * offset_h)

    def norm_offset_x_op(x):
        return (x * width + offset_w) / (width + 2 * offset_w)

    def reverse_y_op(y):
        return y - offset_h

    def reverse_x_op(x):
        return x - offset_w

    def norm_reverse_y_op(y):
        return (y * (height + 2 * offset_h) - offset_h) / height

    def norm_reverse_x_op(x):
        return (x * (width + 2 * offset_w) - offset_w) / width

    if norm_offset_ops:
        offset_ops = (norm_offset_y_op, norm_offset_x_op)
    else:
        offset_ops = (offset_y_op, offset_x_op)

    if norm_reverse_ops:
        reverse_ops = (norm_reverse_y_op, norm_reverse_x_op)
    else:
        reverse_ops = (reverse_y_op, reverse_x_op)

    return padded, offset_ops, reverse_ops
