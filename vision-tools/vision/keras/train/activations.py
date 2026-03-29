from keras import backend as K
from keras.layers import Activation


class ReLU_Max(Activation):
    def __init__(self, activation, **kwargs):
        super(ReLU_Max, self).__init__(activation, **kwargs)
        self.__name__ = 'ReLU_with_max_value'


def relu_with_max_value(x, alpha=0.0, max_value=2.0):
    # Result is truncated to max value
    return K.relu(x, alpha, max_value) - 1
