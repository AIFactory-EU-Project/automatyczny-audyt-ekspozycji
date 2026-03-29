# Code generated with CV Lab
# https://github.com/cvlab-ai/cvlab


### imports ###
import cv2
import numpy as np

from copy import copy
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
            if self._value is None or (self._type == Data.IMAGE and hasattr(self.value, "size") and not self._value.size):
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

def opencvauto_sobel(inputs, outputs, parameters):
    src = inputs['src'].value
    ddepth = parameters['ddepth']
    dx = parameters['dx']
    dy = parameters['dy']
    ksize = parameters['ksize']
    scale = parameters['scale']
    delta = parameters['delta']
    borderType = parameters['borderType']
    dst = cv2.Sobel(src=src, ddepth=ddepth, dx=dx, dy=dy, ksize=ksize, scale=scale, delta=delta,
                    borderType=borderType)
    outputs['dst'] = Data(dst)


# inner code for codeelement75008166
def codeelement75008166_fun(image, parameters, memory):
    image = image.max(axis=2)
    image[image < 5] = 0
    return image


# memory for codeelement75008166
codeelement75008166_memory = {}


# general code for codeelement75008166
def codeelement75008166(inputs, outputs, parameters):
    image = inputs["input"].value
    parameters = {}
    global codeelement75008166_memory
    result = codeelement75008166_fun(image, parameters, codeelement75008166_memory)
    outputs["output"] = Data(result)


# inner code for codeelementex_79755734
def codeelementex_79755734_fun(in1, in2, in3, in4, parameters, memory):
    points = in1.reshape(-1, 2)

    topleft = max(points, key=lambda x: -x[0] - x[1])
    topright = max(points, key=lambda x: x[0] - x[1])

    left = max(points, key=lambda x: -x[0] - x[1] * 0.05)
    right = max(points, key=lambda x: x[0] - x[1] * 0.05)

    bottomleft = max(points, key=lambda x: -x[0] + x[1])
    bottomright = max(points, key=lambda x: x[0] + x[1])

    points = [topleft, topright, right, bottomright, bottomleft, left]
    margin = 10

    o = in4 / 2
    cv2.polylines(o, np.array([points]), True, (255, 255, 255))

    crop_lt = np.min(points, axis=0) - margin
    crop_rb = np.max(points, axis=0) + margin

    o = o[crop_lt[1]:crop_rb[1] + 1, crop_lt[0]:crop_rb[0] + 1]

    o_orig = in4 + 0
    o_orig = o_orig[crop_lt[1]:crop_rb[1] + 1, crop_lt[0]:crop_rb[0] + 1]

    scale = (np.float32(in3.shape) / in4.shape)[:2].mean()
    i = in3
    i = i[int(crop_lt[1] * scale):int(crop_rb[1] * scale) + 1, int(crop_lt[0] * scale):int(crop_rb[0] * scale) + 1]
    p = (np.array(points) - (crop_lt[0], crop_lt[1])) * scale

    return o, o_orig, i, p


# memory for codeelementex_79755734
codeelementex_79755734_memory = {}


# general code for codeelementex_79755734
def codeelementex_79755734(inputs, outputs, parameters):
    ins = [None] * 4
    for i in range(4):
        n = "in" + str(i + 1)
        if n in inputs and inputs[n]:
            ins[i] = inputs[n].value
    o = codeelementex_79755734_fun(ins[0], ins[1], ins[2], ins[3], parameters, codeelementex_79755734_memory)
    for i, v in enumerate(o):
        n = "o" + str(i + 1)
        outputs[n] = Data(v)


def resizer(inputs, outputs, parameters):
    outputs["output"] = Data(cv2.resize(inputs["input"].value, (parameters["width"], parameters["height"])))


# inner code for codeelementex_79737558
def codeelementex_79737558_fun(in1, in2, in3, in4, parameters, memory):
    margin = 30

    def order_points(pts):
        # initialzie a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        rect = np.zeros((4, 2), dtype="float32")

        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # return the ordered coordinates
        return rect

    def four_point_transform(image, rect):
        # obtain a consistent order of the points and unpack them
        # individually
        # rect = order_points(rect)
        rect = rect.astype(np.float32)
        (tl, tr, br, bl) = rect

        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [margin, margin],
            [maxWidth - 1 + margin, margin],
            [maxWidth - 1 + margin, maxHeight - 1 + margin],
            [margin, maxHeight - 1 + margin]], dtype="float32")

        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth + margin * 2, maxHeight + margin * 2))

        # return the warped image
        return warped

    faces = [four_point_transform(in1, in2[i]) for i in range(2)]
    return faces


# memory for codeelementex_79737558
codeelementex_79737558_memory = {}


# general code for codeelementex_79737558
def codeelementex_79737558(inputs, outputs, parameters):
    ins = [None] * 4
    for i in range(4):
        n = "in" + str(i + 1)
        if n in inputs and inputs[n]:
            ins[i] = inputs[n].value
    o = codeelementex_79737558_fun(ins[0], ins[1], ins[2], ins[3], parameters, codeelementex_79737558_memory)
    for i, v in enumerate(o):
        n = "o" + str(i + 1)
        outputs[n] = Data(v)


# inner code for codeelementex_75028295
def codeelementex_75028295_fun(in1, in2, in3, in4, parameters, memory):
    image = in1
    topleft, topright, right, bottomright, bottomleft, left = np.array(in2, int)
    horiz_lines = in3 + 0

    def align(left, right, gradleft, gradright):
        scale = float(in1.shape[0]) / in3.shape[0]

        horiz_left = int(left[1] / scale)
        horiz_miny = max(horiz_left - 10, 0)
        horiz_maxy = min(horiz_left + 20, horiz_lines.shape[0])
        horiz_left = gradleft[horiz_miny:horiz_maxy]
        horiz_left = np.argmax(horiz_left, axis=0) + horiz_miny
        horiz_left = np.int32(horiz_left * scale)

        horiz_right = int(horiz_left / scale)
        horiz_miny = max(horiz_right - 5, 0)
        horiz_maxy = min(horiz_right + 5, horiz_lines.shape[0])
        horiz_right = gradright[horiz_miny:horiz_maxy]
        horiz_right = np.argmax(horiz_right, axis=0) + horiz_miny
        horiz_right = np.int32(horiz_right * scale)

        left = (left[0], horiz_left)
        right = (right[0], horiz_right)

        return left, right

    def angle(b, a, c):
        from math import sqrt, acos, pi
        ab = sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        ac = sqrt((a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2)
        bc = sqrt((c[0] - b[0]) ** 2 + (c[1] - b[1]) ** 2)
        return acos((ab ** 2 + ac ** 2 - bc ** 2) / (2 * ab * ac)) * 180 / pi

    topleft = (topleft[0], min(topleft[1], topright[1]))
    topright = (topright[0], min(topleft[1], topright[1]))

    # left, right = align(left, right, horiz_lines[:,0], horiz_lines[:,-1])
    # bottomright, bottomleft = align(bottomright, bottomleft, horiz_lines[:,-1], horiz_lines[:,0])

    # bottomleft = (bottomleft[0], max(bottomleft[1],bottomright[1]))
    # bottomright = (bottomright[0], max(bottomleft[1],bottomright[1]))

    if angle(topleft, left, bottomleft) > 170:
        left = (left[0], right[1])

    if angle(topright, right, bottomright) > 170:
        right = (right[0], left[1])

    if not 70 < angle(bottomleft, left, right) < 110:
        left = (left[0], right[1])

    if not 70 < angle(left, right, bottomright) < 110:
        right = (right[0], left[1])

    o = image / 2
    cv2.polylines(o, np.array([[topleft, topright, right, bottomright, bottomleft, left]]), True, (255, 255, 255), 3)
    cv2.polylines(o, np.array([[left, right]]), False, (255, 255, 255), 3)

    faces = [
        [topleft, topright, right, left],  # top
        [left, right, bottomright, bottomleft],  # front
    ]

    return o, np.array(faces),


# memory for codeelementex_75028295
codeelementex_75028295_memory = {}


# general code for codeelementex_75028295
def codeelementex_75028295(inputs, outputs, parameters):
    ins = [None] * 4
    for i in range(4):
        n = "in" + str(i + 1)
        if n in inputs and inputs[n]:
            ins[i] = inputs[n].value
    o = codeelementex_75028295_fun(ins[0], ins[1], ins[2], ins[3], parameters, codeelementex_75028295_memory)
    for i, v in enumerate(o):
        n = "o" + str(i + 1)
        outputs[n] = Data(v)


def maxoperator(inputs, outputs, parameters):
    temp = None
    for input_ in inputs.values():
        if temp is None:
            temp = copy(input_.value)
        else:
            temp = np.maximum(temp, input_.value)
    outputs["output"] = Data(temp)


# inner code for codeelementex_74998798
def codeelementex_74998798_fun(in1, in2, in3, in4, parameters, memory):
    contours, _ = cv2.findContours(in1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)
    contour = cv2.convexHull(contour)

    o = in2 / 2
    o = cv2.drawContours(o, [contour], -1, (255, 255, 255))

    c = np.zeros_like(in1)
    c = cv2.drawContours(c, [contour], -1, 255)

    return o, c, contour, None


# memory for codeelementex_74998798
codeelementex_74998798_memory = {}


# general code for codeelementex_74998798
def codeelementex_74998798(inputs, outputs, parameters):
    ins = [None] * 4
    for i in range(4):
        n = "in" + str(i + 1)
        if n in inputs and inputs[n]:
            ins[i] = inputs[n].value
    o = codeelementex_74998798_fun(ins[0], ins[1], ins[2], ins[3], parameters, codeelementex_74998798_memory)
    for i, v in enumerate(o):
        n = "o" + str(i + 1)
        outputs[n] = Data(v)


def opencvdilate(inputs, outputs, parameters):
    image = np.copy(inputs["input"].value)
    element_type = parameters["element type"]
    element_size = parameters["element size"]
    iterations = parameters["iterations"]

    element = cv2.getStructuringElement(element_type, (element_size, element_size))
    image = cv2.dilate(image, element, iterations=iterations)
    outputs["output"] = Data(image)


# inner code for codeelement75013504
def codeelement75013504_fun(image, parameters, memory):
    image = image[:, 20:-20]
    image = cv2.absdiff(image, 128)
    image = cv2.resize(image, (5, image.shape[0]))
    image = cv2.blur(image, (5, 5), borderType=cv2.BORDER_REPLICATE)
    return image


# memory for codeelement75013504
codeelement75013504_memory = {}


# general code for codeelement75013504
def codeelement75013504(inputs, outputs, parameters):
    image = inputs["input"].value
    parameters = {}
    global codeelement75013504_memory
    result = codeelement75013504_fun(image, parameters, codeelement75013504_memory)
    outputs["output"] = Data(result)


def minusoperator(inputs, outputs, parameters):
    outputs["output"] = Data(cv2.subtract(inputs["from"].value, inputs["what"].value))


def forwarder(inputs, outputs, parameters):
    outputs['output'] = inputs['input']


# inner code for codeelement79774782
def codeelement79774782_fun(image, parameters, memory):
    image = (image > image.mean() * 3).astype(np.uint8) * 255
    return image

    mask = image > 10
    mean = image[mask].mean()
    std = image[mask].std()

    omean = 0
    ostd = 200

    image = ((image.astype(np.float32) - mean) / std * ostd + omean).clip(0, 255).astype(np.uint8)
    image = image.max(axis=2)

    return image


# memory for codeelement79774782
codeelement79774782_memory = {}


# general code for codeelement79774782
def codeelement79774782(inputs, outputs, parameters):
    image = inputs["input"].value
    parameters = {}
    global codeelement79774782_memory
    result = codeelement79774782_fun(image, parameters, codeelement79774782_memory)
    outputs["output"] = Data(result)


def opencvauto_canny(inputs, outputs, parameters):
    image = inputs['image'].value
    threshold1 = parameters['threshold1']
    threshold2 = parameters['threshold2']
    apertureSize = parameters['apertureSize']
    L2gradient = parameters['L2gradient']
    edges = cv2.Canny(image=image, threshold1=threshold1, threshold2=threshold2, apertureSize=apertureSize,
                      L2gradient=L2gradient)
    outputs['edges'] = Data(edges)


def opencvmorphologyex(inputs, outputs, parameters):
    image = np.copy(inputs["input"].value)
    operation = parameters["operation"]
    element_type = parameters["element type"]
    element_size = parameters["element size"]
    iterations = parameters["iterations"]

    element = cv2.getStructuringElement(element_type, (element_size, element_size))
    image = cv2.morphologyEx(image, operation, element, iterations=iterations, )
    outputs["output"] = Data(image)


def colorconverter(inputs, outputs, parameters):
    if parameters["code"] is None:
        outputs["output"] = Data(inputs["input"].value.copy())
    else:
        outputs["output"] = Data(cv2.cvtColor(inputs["input"].value, parameters["code"]))


### process function ###

def process(imageloader14_output, imageloader12_output):
    imageloader12 = {"output": imageloader12_output}
    resizer11 = {}
    resizer({"input": imageloader12["output"]}, resizer11, {"width": 3840, "height": 2560})
    imageloader14 = {"output": imageloader14_output}
    resizer13 = {}
    resizer({"input": imageloader14["output"]}, resizer13, {"width": 3840, "height": 2560})
    minusoperator10 = {}
    minusoperator({"what": resizer13["output"], "from": resizer11["output"]}, minusoperator10, {})
    codeelement9 = {}
    codeelement75008166({"input": minusoperator10["output"]}, codeelement9, {"code": u'import cv2 as cv\nimport numpy as np\nimage = image.max(axis=2)\nimage[image<5] = 0\nreturn image', "split_channels": False})
    opencvauto_canny8 = {}
    opencvauto_canny({"image": codeelement9["output"]}, opencvauto_canny8, {"threshold1": 30815.0, "threshold2": 13039.0, "apertureSize": 7, "L2gradient": 1})
    opencvdilate7 = {}
    opencvdilate({"input": opencvauto_canny8["edges"]}, opencvdilate7, {"element type": 2, "element size": 7, "iterations": 1})
    codeelement15 = {}
    codeelement79774782({"input": codeelement9["output"]}, codeelement15, {
        "code": u'import cv2 as cv\nimport numpy as np\n\nimage = (image>image.mean()*3).astype(np.uint8)*255\n\nreturn image\n\nmask = image > 10\nmean = image[mask].mean()\nstd = image[mask].std()\n\nomean = 0\nostd = 200\n\nimage = ((image.astype(np.float32)-mean)/std*ostd+omean).clip(0,255).astype(np.uint8)\nimage = image.max(axis=2)\n\nreturn image',
        "split_channels": False})
    maxoperator6 = {}
    maxoperator({"inputs0": opencvdilate7["output"], "inputs1": codeelement15["output"]}, maxoperator6, {})
    opencvmorphologyex5 = {}
    opencvmorphologyex({"input": maxoperator6["output"]}, opencvmorphologyex5, {"operation": 2, "element type": 2, "element size": 7, "iterations": 1})
    opencvmorphologyex4 = {}
    opencvmorphologyex({"input": opencvmorphologyex5["output"]}, opencvmorphologyex4, {"operation": 3, "element type": 2, "element size": 1, "iterations": 1})
    forwarder16 = {}
    forwarder({"input": minusoperator10["output"]}, forwarder16, {})
    codeelementex3 = {}
    codeelementex_74998798({"in1": opencvmorphologyex4["output"], "in2": forwarder16["output"]}, codeelementex3, {
        "code": u'import cv2 as cv\nimport numpy as np\n\n_ , contours, _ = cv.findContours(in1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)\n\ncontour = max(contours, key=cv.contourArea)\ncontour = cv.convexHull(contour)\n\no = in2 / 2\no = cv.drawContours(o, [contour], -1, (255,255,255))\n\nc = np.zeros_like(in1)\nc = cv.drawContours(c, [contour], -1, 255)\n\nreturn o, c, contour, None',
        "split_channels": False})
    forwarder17 = {}
    forwarder({"input": resizer11["output"]}, forwarder17, {})
    codeelementex2 = {}
    codeelementex_79755734({"in4": forwarder16["output"], "in1": codeelementex3["o3"], "in3": forwarder17["output"]}, codeelementex2, {
        "code": u'import cv2 as cv\nimport numpy as np\n\npoints = in1.reshape(-1,2)\n\ntopleft = max(points, key=lambda(x,y): -x-y)\ntopright = max(points, key=lambda(x,y): +x-y)\n\nleft = max(points, key=lambda(x,y): -x-y*0.05)\nright = max(points, key=lambda(x,y): x-y*0.05)\n\nbottomleft = max(points, key=lambda(x,y): -x+y)\nbottomright = max(points, key=lambda(x,y): x+y)\n\npoints = [topleft, topright, right, bottomright, bottomleft, left]\nmargin = 10\n\no = in4/2\ncv.polylines(o, np.array([points]), True, (255,255,255))\n\ncrop_lt = np.min(points,axis=0)-margin\ncrop_rb = np.max(points,axis=0)+margin\n\no = o[crop_lt[1]:crop_rb[1]+1,crop_lt[0]:crop_rb[0]+1]\n\no_orig = in4 + 0\no_orig = o_orig[crop_lt[1]:crop_rb[1]+1,crop_lt[0]:crop_rb[0]+1]\n\nscale = (np.float32(in3.shape)/in4.shape)[:2].mean()\ni = in3\ni = i[int(crop_lt[1]*scale):int(crop_rb[1]*scale)+1,int(crop_lt[0]*scale):int(crop_rb[0]*scale)+1]\np = (np.array(points) - (crop_lt[0],crop_lt[1]))*scale\n\nreturn o, o_orig, i, p',
        "split_channels": False})
    colorconverter21 = {}
    colorconverter({"input": codeelementex2["o2"]}, colorconverter21, {"code": 6})
    opencvauto_sobel20 = {}
    opencvauto_sobel({"src": colorconverter21["output"]}, opencvauto_sobel20, {"ddepth": 0, "dx": 0, "dy": 1, "ksize": 13, "scale": 1e-06, "delta": 128.0, "borderType": 0})
    codeelement19 = {}
    codeelement75013504({"input": opencvauto_sobel20["dst"]}, codeelement19,
                        {"code": u'import cv2 as cv\nimport numpy as np\nimage = image[:,20:-20]\nimage = cv.absdiff(image, 128)\nimage = cv.resize(image, (5, image.shape[0]))\nimage = cv.blur(image, (5,5), borderType=cv.BORDER_REPLICATE)\nreturn image', "split_channels": False})
    codeelementex18 = {}
    codeelementex_75028295({"in1": codeelementex2["o3"], "in2": codeelementex2["o4"], "in3": codeelement19["output"]}, codeelementex18, {
        "code": u'import cv2 as cv\nimport numpy as np\n\nimage = in1\ntopleft, topright, right, bottomright, bottomleft, left = np.array(in2, int)\nhoriz_lines = in3 + 0\n\ndef align(left, right, gradleft, gradright):\n\tscale = float(in1.shape[0]) / in3.shape[0]\n\n\thoriz_left = int(left[1]/scale)\n\thoriz_miny = max(horiz_left-10, 0)\n\thoriz_maxy = min(horiz_left+20, horiz_lines.shape[0])\n\thoriz_left = gradleft[horiz_miny:horiz_maxy]\n\thoriz_left = np.argmax(horiz_left, axis=0) + horiz_miny\n\thoriz_left = np.int32(horiz_left*scale)\n\n\thoriz_right = int(horiz_left/scale)\n\thoriz_miny = max(horiz_right-5, 0)\n\thoriz_maxy = min(horiz_right+5, horiz_lines.shape[0])\n\thoriz_right = gradright[horiz_miny:horiz_maxy]\n\thoriz_right = np.argmax(horiz_right, axis=0) + horiz_miny\n\thoriz_right = np.int32(horiz_right*scale)\n\n\tleft = (left[0], horiz_left)\n\tright = (right[0], horiz_right)\n\t\n\treturn left, right\n\ndef angle(b, a, c):\n\tfrom math import sqrt, acos, pi\n\tab = sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )\n\tac = sqrt( (a[0]-c[0])**2 + (a[1]-c[1])**2 )\n\tbc = sqrt( (c[0]-b[0])**2 + (c[1]-b[1])**2 )\n\treturn acos( (ab**2+ac**2-bc**2) / (2*ab*ac) ) * 180 / pi \n\ntopleft = (topleft[0], min(topleft[1],topright[1]))\ntopright = (topright[0], min(topleft[1],topright[1]))\n\n#left, right = align(left, right, horiz_lines[:,0], horiz_lines[:,-1])\n#bottomright, bottomleft = align(bottomright, bottomleft, horiz_lines[:,-1], horiz_lines[:,0])\n\n#bottomleft = (bottomleft[0], max(bottomleft[1],bottomright[1]))\n#bottomright = (bottomright[0], max(bottomleft[1],bottomright[1]))\n\nif angle(topleft, left, bottomleft) > 170:\n\tleft = (left[0], right[1])\n\nif angle(topright, right, bottomright) > 170:\n\tright = (right[0], left[1])\n\nif not 70 < angle(bottomleft, left, right) < 110:\n\tleft = (left[0], right[1])\n\nif not 70 < angle(left, right, bottomright) < 110:\n\tright = (right[0], left[1])\n\no = image / 2\ncv.polylines(o, np.array([[topleft, topright, right, bottomright, bottomleft, left]]), True, (255,255,255), 3)\ncv.polylines(o, np.array([[left,right]]), False, (255,255,255), 3)\n\nfaces = [\n\t[topleft, topright, right, left],       #top\n\t[left, right, bottomright, bottomleft], #front\n]\n\nreturn o, np.array(faces),',
        "split_channels": False})
    codeelementex1 = {}
    codeelementex_79737558({"in1": codeelementex2["o3"], "in2": codeelementex18["o2"]}, codeelementex1, {
        "code": u'import numpy as np\nimport cv2\n\nmargin = 30\n\ndef order_points(pts):\n\t# initialzie a list of coordinates that will be ordered\n\t# such that the first entry in the list is the top-left,\n\t# the second entry is the top-right, the third is the\n\t# bottom-right, and the fourth is the bottom-left\n\trect = np.zeros((4, 2), dtype = "float32")\n\n\t# the top-left point will have the smallest sum, whereas\n\t# the bottom-right point will have the largest sum\n\ts = pts.sum(axis = 1)\n\trect[0] = pts[np.argmin(s)]\n\trect[2] = pts[np.argmax(s)]\n\n\t# now, compute the difference between the points, the\n\t# top-right point will have the smallest difference,\n\t# whereas the bottom-left will have the largest difference\n\tdiff = np.diff(pts, axis = 1)\n\trect[1] = pts[np.argmin(diff)]\n\trect[3] = pts[np.argmax(diff)]\n\n\t# return the ordered coordinates\n\treturn rect\n\ndef four_point_transform(image, rect):\n\t# obtain a consistent order of the points and unpack them\n\t# individually\n\t#rect = order_points(rect)\n\trect = rect.astype(np.float32)\n\t(tl, tr, br, bl) = rect\n\n\t# compute the width of the new image, which will be the\n\t# maximum distance between bottom-right and bottom-left\n\t# x-coordiates or the top-right and top-left x-coordinates\n\twidthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))\n\twidthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))\n\tmaxWidth = max(int(widthA), int(widthB))\n\n\t# compute the height of the new image, which will be the\n\t# maximum distance between the top-right and bottom-right\n\t# y-coordinates or the top-left and bottom-left y-coordinates\n\theightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))\n\theightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))\n\tmaxHeight = max(int(heightA), int(heightB))\n\n\t# now that we have the dimensions of the new image, construct\n\t# the set of destination points to obtain a "birds eye view",\n\t# (i.e. top-down view) of the image, again specifying points\n\t# in the top-left, top-right, bottom-right, and bottom-left\n\t# order\n\tdst = np.array([\n\t\t[margin, margin],\n\t\t[maxWidth - 1+margin, margin],\n\t\t[maxWidth - 1+margin, maxHeight - 1+margin],\n\t\t[margin, maxHeight - 1+margin]], dtype = "float32")\n\n\t# compute the perspective transform matrix and then apply it\n\tM = cv2.getPerspectiveTransform(rect, dst)\n\twarped = cv2.warpPerspective(image, M, (maxWidth+margin*2, maxHeight+margin*2))\n\n\t# return the warped image\n\treturn warped\n\nfaces = [four_point_transform(in1, in2[i]) for i in xrange(2)]\n\nreturn faces',
        "split_channels": False})

    return codeelementex1


### script ###

if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        print("Usage: generated.py imageloader14_output, imageloader12_output")
        exit(1)

    args = []
    for arg in sys.argv[1:]:
        args.append(Data(cv2.imread(arg)))
    outputs = process(*args)
    for name, output in outputs.items():
        cv2.imwrite("output-{}.png".format(name), output.value)
