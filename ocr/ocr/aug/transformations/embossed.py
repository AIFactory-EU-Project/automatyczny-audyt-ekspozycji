#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Code generated with CV Lab
# https://github.com/cvlab-ai/cvlab
#


### imports ###

from __future__ import print_function, unicode_literals

# from exceptions import TypeError
import cv2 as cv
from threading import RLock


### helpers ###

class Data(object):
    NONE = 0
    SEQUENCE = 1
    IMAGE = 2

    def __init__(self, value=None, _type=IMAGE):
        self._type = _type
        if _type == Data.SEQUENCE and value is None:
            self._value = []
        else:
            self._value = value
        self.lock = RLock()

    def clear(self):
        with self.lock:
            if self._type == Data.SEQUENCE:
                for d in self._value:
                    d.clear()
            else:
                self.value = None

    def copy(self):
        with self.lock:
            if self._type == self.NONE:
                return EmptyData()
            if self._type == self.SEQUENCE:
                return Sequence([d.copy() for d in self._value])
            elif self._type == self.IMAGE:
                if self._value is None or (hasattr(self._value, "size") and not len(self._value)):
                    pass
                    # print("Copying null data!")
                return ImageData(self._value)
            else:
                raise TypeError("Wrong Data.type")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        with self.lock:
            if self._value is new_value:
                return
            self._value = new_value

    def assign(self, other):
        assert isinstance(other, Data)
        assert self.is_compatible(other)  # todo: assert czy raise?
        if self._type == Data.SEQUENCE:
            assert len(self._value) == len(other._value)  # todo: jak wyĹĽej
            for mine, her in zip(self._value, other._value):
                mine.assign(her)
        else:
            self.value = other.value

    def is_compatible(self, other):
        assert isinstance(other, Data)
        if self._type != other._type: return False
        if self._type == Data.SEQUENCE:
            if len(self._value) != len(other._value): return False
            return all(mine.is_compatible(her) for mine, her in zip(self._value, other._value))
        return True

    def type(self):
        with self.lock:
            if self._value is None or (
                    self._type == Data.IMAGE and hasattr(self.value, "size") and not self._value.size):
                return Data.NONE
            else:
                return self._type

    def sequence_get_value(self, sequence_number):
        with self.lock:
            if self.type() != Data.SEQUENCE:
                return self
            else:
                return self._value[min(sequence_number, len(self._value) - 1)]

    __getitem__ = sequence_get_value

    def __iter__(self):
        with self.lock:
            if self.type() == Data.NONE:
                return iter([])
            elif self.type() == Data.SEQUENCE:
                return iter(self._value)
            else:
                return iter([self])

    def desequence_all(self):
        with self.lock:
            if self._type == Data.NONE: return [None]
            if self._type == Data.IMAGE: return [self._value]
            if self._type == Data.SEQUENCE:
                t = []
                for d in self._value:
                    t += d.desequence_all()
                return t
            raise TypeError("Wrong data type - cannot desequence")

    def is_complete(self):
        with self.lock:
            t = self.type()
            if t == Data.NONE:
                return False
            elif t == Data.IMAGE:
                return True
            else:
                return all(d.is_complete() for d in self._value)

    def create_placeholder(self):
        if self._type == Data.SEQUENCE:
            return Data([d.create_placeholder() for d in self._value], Data.SEQUENCE)
        else:
            return Data()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        id_ = "0x{:08X}".format(id(self))
        if self._type == Data.NONE: return '<Data [empty] at {}>'.format(id_)
        if self.type() == Data.IMAGE:
            try:
                shape = "?"
                shape = len(self._value)
                shape = self._value.shape
            except Exception:
                pass
            return '<Data [image {}] at {}>'.format(shape, id_)
        if self.type() == Data.NONE: return "<Data [empty image] at {}>".format(id_)
        if self.type() == Data.SEQUENCE:
            s = ""
            images_count = 0
            none_count = 0
            for d in self._value:
                if d.type() == Data.SEQUENCE:
                    s += str(d) + ", "
                if d.type() == Data.IMAGE:
                    images_count += 1
                if d.type() == Data.NONE:
                    none_count += 1
            if images_count:
                s += str(images_count) + " images, "
            if none_count:
                s += str(none_count) + " nones, "
            if len(s) > 0:
                s = s.rstrip(', ')
            s = '<Sequence ' + '[' + s + '] at {}>'.format(id_)
            return s
        raise TypeError("Wrong data type - cannot desequence")

    def __nonzero__(self):
        return self.type() != Data.NONE

    ready = __nonzero__

    def __eq__(self, other):
        if not isinstance(other, Data): return False
        with self.lock, other.lock:
            if self.type() != other.type(): return False
            if self.type() == Data.SEQUENCE:
                if len(self._value) != len(other._value): return False
                assert all(isinstance(d, Data) for d in self._value)
                assert all(isinstance(d, Data) for d in other._value)
                return all(a == b for a, b in zip(self._value, other._value))
            else:
                return self._value is other._value
                # todo: if we want logical equality rather than reference equality, we shall use this:
                # elif self.type() == Data.IMAGE:
                # #assert isinstance(self._value, np.ndarray)
                # return self._value is other._value and np.array_equal(self._value, other._value)
                # else:
                #     raise ValueError("Wrong data type")


class EmptyOptionalData(Data):
    def ready(self):
        return True


def Sequence(values=None):
    return Data(values, Data.SEQUENCE)


def EmptyData():
    return Data(None, Data.NONE)


def ImageData(value=None):
    return Data(value, Data.IMAGE)


### functions ###


# inner code for codeelement86093829
def codeelement86093829_fun(image, parameters, memory):
    import cv2 as cv
    import numpy as np
    import random

    angle = random.uniform(0, 360)

    image = image.mean(axis=2).astype(np.uint8)

    def rotate(image, angle):
        M = cv.getRotationMatrix2D((image.shape[1] / 2, image.shape[0] / 2), angle, 1)
        return cv.warpAffine(image, M, (image.shape[1], image.shape[0]))

    def get_kernel(angle):
        kernel = np.array([
            [0, 1, 2, 1, 0],
            [1, 2, 4, 2, 1],
            [0, 0, 0, 0, 0],
            [-1, -2, -4, -2, -1],
            [0, -1, -2, -1, 0],
        ], dtype=np.float)

        #    kernel2 = np.array([
        #     [ 0, 1, 2, 1, 0],
        #     [ 1, 2, 3, 2, 1],
        #     [ 1, 2, 5, 2, 1],
        #     [ 0, 0, 0, 0, 0],
        #     [-1,-2,-5,-2,-1],
        #     [-1,-2,-3,-2,-1],
        #     [ 0,-1,-2,-1, 0],
        #    ], dtype=np.float)

        #    kernel2 = np.array([
        #     [ 1, 2, 1],
        #     [ 0, 0, 0],
        #     [ -1,-2,-1],
        #    ], dtype=np.float)

        # kernel2 *= 0.2
        return rotate(kernel, angle)

    kernel = get_kernel(angle)
    image = cv.filter2D(image.astype(np.float32), -1, kernel, anchor=(-1, -1))

    return image / image.max()


# memory for codeelement86093829
codeelement86093829_memory = {}


# general code for codeelement86093829
def codeelement86093829(inputs, outputs, parameters):
    image = inputs["input"].value
    parameters = {}
    global codeelement86093829_memory
    result = codeelement86093829_fun(image, parameters, codeelement86093829_memory)
    outputs["output"] = Data(result)


# inner code for codeelementex_68680519
def codeelementex_68680519_fun(in1, in2, in3, in4, parameters, memory):
    import cv2 as cv
    import numpy as np
    import random
    from vision.aug.transformations.contours_adder import ContoursAdderTransformation

    # coefficient of occurency of paint

    orig_coef = random.uniform(0, .7) if random.random() < .5 else 0
    # probability of occurency of ditorted paint
    distorted = .5

    mask_coef = random.uniform(50, 200)

    image = in1.astype(np.float32)
    mask = cv.cvtColor(in2, cv.COLOR_GRAY2BGR)
    mask *= mask_coef
    mask2 = in3
    bg = in4

    mask2 = cv.cvtColor(mask2, cv.COLOR_GRAY2BGR)

    if random.random() < distorted:
        mask2 = ContoursAdderTransformation.draw_random_contour(image=mask2, color=[0, 0, 0], limit=1000,
                                                                iterations=random.randint(1, 10))

    image = np.where(mask2 > 0, (image * orig_coef + bg * (1 - orig_coef)) * (mask2 / 255.) + (1 - mask2 / 255.) * bg,
                     bg)
    out = cv.add(image, mask, dtype=0)

    return out, mask2


# memory for codeelementex_68680519
codeelementex_68680519_memory = {}


# general code for codeelementex_68680519
def codeelementex_68680519(inputs, outputs, parameters):
    ins = [None] * 4
    for i in range(4):
        n = "in" + str(i + 1)
        if n in inputs and inputs[n]:
            ins[i] = inputs[n].value
    o = codeelementex_68680519_fun(ins[0], ins[1], ins[2], ins[3], parameters, codeelementex_68680519_memory)
    for i, v in enumerate(o):
        n = "o" + str(i + 1)
        outputs[n] = Data(v)


# inner code for codeelementex_21307767
def codeelementex_21307767_fun(in1, in2, in3, in4, parameters, memory):
    import cv2 as cv
    import numpy as np

    margin = 5

    image = in1[..., 0:3]
    mask = in1[..., 3]
    bg = in3

    size = (image.shape[1] - margin * 2, image.shape[0] - margin * 2)

    image_out = np.zeros_like(image) + 255
    image_out[margin:-margin, margin:-margin] = cv.resize(image, size, interpolation=cv.INTER_LANCZOS4)

    mask_out = np.zeros_like(mask)
    mask_out[margin:-margin, margin:-margin] = cv.resize(mask, size)

    return image_out, mask_out, bg

    # DODAWANIE MARGINESU - USUNIETE
    color = np.array((255, 255, 255), dtype=np.uint8)
    margin = 10

    image = in1
    mask = in2

    image_out = np.zeros((image.shape[0] + margin * 2, image.shape[1] + margin * 2, 3), dtype=np.uint8)
    image_out += color
    image_out[margin:image.shape[0] + margin, margin:image.shape[1] + margin] = image

    mask_out = np.zeros((mask.shape[0] + margin * 2, mask.shape[1] + margin * 2), dtype=np.uint8)
    mask_out[margin:mask.shape[0] + margin, margin:mask.shape[1] + margin] = mask

    return image_out, mask_out


# memory for codeelementex_21307767
codeelementex_21307767_memory = {}


# general code for codeelementex_21307767
def codeelementex_21307767(inputs, outputs, parameters):
    ins = [None] * 4
    for i in range(4):
        n = "in" + str(i + 1)
        if n in inputs and inputs[n]:
            ins[i] = inputs[n].value
    o = codeelementex_21307767_fun(ins[0], ins[1], ins[2], ins[3], parameters, codeelementex_21307767_memory)
    for i, v in enumerate(o):
        n = "o" + str(i + 1)
        outputs[n] = Data(v)


# inner code for codeelementex_86090558
def codeelementex_86090558_fun(in1, in2, in3, in4, parameters, memory):
    import cv2 as cv
    import numpy as np
    import random

    image = in1
    mask = in2

    sigma = 4 * random.uniform(0, 1) ** 5

    image = cv.GaussianBlur(image, (11, 11), sigma, sigma, 2)
    mask = cv.GaussianBlur(mask, (11, 11), sigma, sigma, 2) ** 1.15
    mask = mask.clip(0, 255).astype(np.uint8)

    return image, mask


# memory for codeelementex_86090558
codeelementex_86090558_memory = {}


# general code for codeelementex_86090558
def codeelementex_86090558(inputs, outputs, parameters):
    ins = [None] * 4
    for i in range(4):
        n = "in" + str(i + 1)
        if n in inputs and inputs[n]:
            ins[i] = inputs[n].value
    o = codeelementex_86090558_fun(ins[0], ins[1], ins[2], ins[3], parameters, codeelementex_86090558_memory)
    for i, v in enumerate(o):
        n = "o" + str(i + 1)
        outputs[n] = Data(v)


### process function ###

def process(imageloader3_output, imageloader4_output):
    imageloader3 = {"output": imageloader3_output}
    imageloader4 = {"output": imageloader4_output}
    codeelementex2 = {}
    codeelementex_21307767({"in1": imageloader3["output"], "in3": imageloader4["output"]}, codeelementex2, {
        "code": u'import cv2 as cv\nimport numpy as np\n\nmargin = 5\n\nimage = in1[...,0:3]\nmask = in1[...,3]\nbg = in3\n\nsize = (image.shape[1]-margin*2, image.shape[0]-margin*2)\n\nimage_out = np.zeros_like(image) + 255\nimage_out[margin:-margin,margin:-margin] = cv.resize(image, size, interpolation=cv.INTER_LANCZOS4)\n\nmask_out = np.zeros_like(mask)\nmask_out[margin:-margin,margin:-margin] = cv.resize(mask, size)\n\nreturn image_out, mask_out, bg\n\n\n# DODAWANIE MARGINESU - USUNIETE\ncolor = np.array((255,255,255), dtype=np.uint8)\nmargin = 10\n\nimage = in1\nmask = in2\n\nimage_out = np.zeros((image.shape[0]+margin*2,image.shape[1]+margin*2,3), dtype=np.uint8)\nimage_out += color\nimage_out[margin:image.shape[0]+margin,margin:image.shape[1]+margin] = image\n\nmask_out = np.zeros((mask.shape[0]+margin*2,mask.shape[1]+margin*2), dtype=np.uint8)\nmask_out[margin:mask.shape[0]+margin,margin:mask.shape[1]+margin] = mask\n\nreturn image_out, mask_out',
        "split_channels": False})
    codeelementex6 = {}
    codeelementex_86090558({"in1": codeelementex2["o1"], "in2": codeelementex2["o2"]}, codeelementex6, {
        "code": u'import cv2 as cv\nimport numpy as np\nimport random\n\nimage = in1\nmask = in2\n\nsigma = 4 * random.uniform(0, 1)**5\n\nimage = cv.GaussianBlur(image, (11, 11), sigma, sigma, 2)\nmask = cv.GaussianBlur(mask, (11, 11), sigma, sigma, 2) ** 1.15\nmask = mask.clip(0,255).astype(np.uint8)\n\nreturn image, mask',
        "split_channels": False})
    codeelement5 = {}
    codeelement86093829({"input": codeelementex6["o1"]}, codeelement5, {
        "code": u'import cv2 as cv\nimport numpy as np\nimport random\n\nangle = random.uniform(0,360)\n\nimage = image.mean(axis=2).astype(np.uint8)\n\ndef rotate(image, angle):\n\tM = cv.getRotationMatrix2D((image.shape[1]/2,image.shape[0]/2),angle,1)\n\treturn cv.warpAffine(image,M,(image.shape[1],image.shape[0]))\n\ndef get_kernel(angle):\n\tkernel = np.array([\n\t [ 0, 1, 2, 1, 0],\n\t [ 1, 2, 4, 2, 1],\n\t [ 0, 0, 0, 0, 0],\n\t [-1,-2,-4,-2,-1],\n \t [ 0,-1,-2,-1, 0],\n\t], dtype=np.float)\n\n#\tkernel2 = np.array([\n#\t [ 0, 1, 2, 1, 0],\n#\t [ 1, 2, 3, 2, 1],\n#\t [ 1, 2, 5, 2, 1],\n#\t [ 0, 0, 0, 0, 0],\n#\t [-1,-2,-5,-2,-1],\n#\t [-1,-2,-3,-2,-1],\n#\t [ 0,-1,-2,-1, 0],\n#\t], dtype=np.float)\n\n\n#\tkernel2 = np.array([\n#\t [ 1, 2, 1],\n#\t [ 0, 0, 0],\n#\t [ -1,-2,-1],\n#\t], dtype=np.float)\n\n\n\t# kernel2 *= 0.2\n\treturn rotate(kernel, angle)\n\nkernel = get_kernel(angle)\nimage = cv.filter2D(image.astype(np.float32), -1, kernel, anchor=(-1,-1))\n\nreturn image/image.max()\n',
        "split_channels": False})
    codeelementex1 = {}
    codeelementex_68680519({"in4": codeelementex2["o3"], "in1": codeelementex2["o1"], "in2": codeelement5["output"],
                            "in3": codeelementex6["o2"]}, codeelementex1, {
                               "code": 'import cv2 as cv\nimport numpy as np\nimport random\t\nfrom ocr.aug.transformations.contours_adder import ContoursAdderTransformation\n\n\n# coefficient of occurency of paint\n\n\norig_coef = random.uniform(0, .7) if random.random() < .5 else 0\n# probability of occurency of ditorted paint\ndistorted = .5\n\n\nmask_coef = random.uniform(50, 200)\n\nimage = in1.astype(np.float32)\nmask = cv.cvtColor(in2, cv.COLOR_GRAY2BGR)\nmask *= mask_coef\nmask2 = in3\nbg = in4\n\nscale = 2\n\nimage = cv.resize(image, (image.shape[1]/scale, image.shape[0]/scale), interpolation=cv.INTER_CUBIC)\nmask2 = cv.resize(mask2, (mask2.shape[1]/scale, mask2.shape[0]/scale), interpolation=cv.INTER_CUBIC)\nmask = cv.resize(mask, (mask.shape[1]/scale, mask.shape[0]/scale), interpolation=cv.INTER_CUBIC)\n\nmask2 = cv.cvtColor(mask2, cv.COLOR_GRAY2BGR)\n\n\n\nif random.random() < distorted:\n\tmask2 = ContoursAdderTransformation.draw_random_contour(image=mask2, color=[0, 0, 0], limit=1000, iterations=random.randint(1, 10))\n\nimage = np.where(mask2 > 0, (image * orig_coef + bg * (1-orig_coef))*(mask2/255.)  + (1 - mask2/255.)*bg, bg)\t\nout = cv.add(image, mask, dtype=0)\n\nreturn out, mask2\n',
                               "split_channels": False})

    return codeelementex1


def emboss(img, bg):
    return process(Data(img), Data(bg))


### script ###

if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        print("Usage: generated.py imageloader3_output, imageloader4_output")
        exit(1)
    args = []
    for arg in sys.argv[1:]:
        args.append(Data(cv.imread(arg)))
    outputs = process(*args)
    for name, output in outputs.items():
        cv.imwrite("output-{}.png".format(name), output.value)
