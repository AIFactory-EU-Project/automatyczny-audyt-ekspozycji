import sys

from keras import Model
from keras.applications import MobileNet, InceptionResNetV2
from keras.applications import MobileNetV2
from keras.applications import NASNetMobile
from keras.initializers import VarianceScaling
from vision.keras.train import activations
from keras import utils
from keras.layers import Reshape, Dropout, Conv2D, Activation, Dense


def get_model(name, class_number, input_shape=(224, 224, 3), activation="softmax", lock_first_layers=1.0, weights=None):
    this_mod = sys.modules[__name__]
    if not hasattr(this_mod, name):
        raise ValueError("No net with name {}".format(name))

    utils.get_custom_objects().update({'relu_with_max_value': activations.ReLU_Max(activations.relu_with_max_value)})

    func = getattr(this_mod, name)
    init_weights, weights = determine_weights(weights)
    model = func(class_number, input_shape, activation, init_weights)
    model.name = name

    if weights is not None:
        model.load_weights(weights)

    block_first_layers(model, lock_first_layers)

    return model


def determine_weights(weights):
    defaults = ["imagenet"]
    return (weights, None) if weights in defaults else (None, weights)


def block_first_layers(model, layers_to_block):
    if isinstance(layers_to_block, float):
        layers_to_block = int(layers_to_block * len(model.layers))

    for i in range(layers_to_block):
        model.layers[i].trainable = False


def mobilenet(class_number, input_shape=(224, 224, 3), activation="softmax", init_weights=None):
    model = MobileNet(input_shape=input_shape, alpha=1.0, depth_multiplier=1, dropout=1e-3,
                      include_top=False, weights=init_weights, input_tensor=None, pooling='avg')

    # add new layers
    init = VarianceScaling(scale=1.0, mode='fan_avg', distribution='uniform')

    current_output = model.layers[-1].output

    current_layer = Reshape((1, 1, 1024))
    current_layer.name = "reshape_1"
    current_output = current_layer(current_output)

    current_layer = Dropout(rate=1e-3)
    current_layer.name = "dropout"
    current_output = current_layer(current_output)

    current_layer = Conv2D(filters=class_number, kernel_size=(1, 1), strides=(1, 1), kernel_initializer=init)
    current_layer.name = "conv_preds"
    current_output = current_layer(current_output)

    current_layer = Activation(activation)
    current_layer.name = "act_{}".format(activation)
    current_output = current_layer(current_output)

    current_layer = Reshape(target_shape=(class_number,))
    current_layer.name = "reshape_2"
    current_output = current_layer(current_output)

    return Model(inputs=[model.input], outputs=[current_output])


def mobilenetv2(class_number, input_shape=(224, 224, 3), activation="softmax", init_weights=None):
    model = MobileNetV2(input_shape=input_shape, alpha=1.0, depth_multiplier=1,
                        include_top=False, weights=init_weights, input_tensor=None, pooling='avg')

    current_output = model.layers[-1].output

    current_layer = Dense(class_number, activation=activation)
    current_layer.name = "dense_{}".format(activation)
    current_output = current_layer(current_output)

    return Model(inputs=[model.input], outputs=[current_output])


def nasnet(class_number, input_shape=(224, 224, 3), activation="softmax", init_weights=None):
    model = NASNetMobile(input_shape=input_shape, include_top=False, weights=init_weights, pooling="avg")

    current_output = model.layers[-1].output

    current_layer = Dense(class_number, activation=activation)
    current_layer.name = "dense_{}".format(activation)
    current_output = current_layer(current_output)

    return Model(inputs=[model.input], outputs=[current_output])


def inception_resnetv2(class_number, input_shape=(224, 244, 3), activation="softmax", init_weights=None):
    model = InceptionResNetV2(include_top=False, weights=init_weights, input_shape=input_shape, pooling="avg")

    current_output = model.layers[-1].output

    current_layer = Dense(class_number, activation=activation)
    current_layer.name = "dense_{}".format(activation)
    current_output = current_layer(current_output)

    return Model(inputs=[model.input], outputs=[current_output])
