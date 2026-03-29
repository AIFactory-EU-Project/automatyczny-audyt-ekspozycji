import random
from collections import OrderedDict


class BaseParam(object):
    pass


class IntParam(BaseParam):

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def get(self):
        return random.randint(self.min, self.max)


class FloatParam(IntParam):

    def get(self):
        return random.uniform(self.min, self.max)


class LogParam(BaseParam):

    def __init__(self, factor, base, min_power, max_power):
        self.factor = factor
        self.base = base
        self.min_power = min_power
        self.max_power = max_power

    def get(self):
        return self.factor * self.base ** random.uniform(self.min_power, self.max_power)


class LogIntParam(LogParam):
    def get(self):
        return int(round(LogParam.get(self)))


class ListParam(BaseParam):

    def __init__(self, list_):
        self.list_ = list_

    def get(self):
        return random.choice(self.list_)


def get_params_dict(params):
    params_set = OrderedDict()
    for p in params:
        params_set[p.name] = p.get()
    return params_set

