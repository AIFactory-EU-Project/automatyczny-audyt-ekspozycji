import numpy as np
import cv2 as cv


def isimage(var):
    if var is None: 
        return False
    if isinstance(var, np.ndarray):
        return var.size > 0
    raise ValueError("Cannot determine type of a variable {}".format(var))


def image_shape(image):
    if not isimage(image): 
        raise ValueError("Variable is not an image")
    if len(image.shape) == 1:
        h = image.shape[0]
        w = ch = 1
    elif len(image.shape) == 2:
        h, w = image.shape
        ch = 1
    elif len(image.shape) == 3:
        h, w, ch = image.shape
    else: 
        raise ValueError("Cannot determine image shape")
    
    return h, w, ch


def merge(images, rows=None, cols=None, background=0):
    if not images:
        return np.array([])

    rows_first = True

    if not rows and not cols:
        cols = int(np.ceil(len(images)**0.5))
    if cols and not rows:
        rows = int(np.ceil(len(images)*1./cols))
    if rows and not cols:
        cols = int(np.ceil(len(images)*1./rows))
        rows_first = False

    h, w, ch = image_shape(images[0])
    dtype = images[0].dtype

    output = np.zeros((h*rows, w*cols, ch), dtype)
    output[...] = background

    for i, image in enumerate(images):
        if image.shape != images[0].shape:
            raise ValueError("Wrong image shape")

        if rows_first:
            y, x = divmod(i, cols)
        else:
            x, y = divmod(i, rows)

        y *= h
        x *= w

        output[y:y+h, x:x+w, ...] = image

    return output


def array_to_pixmap(arr):
    from PyQt4 import QtGui
    arr = arr.astype(np.uint8)
    if len(arr.shape) == 2 or (len(arr.shape) == 3 and arr.shape[2] == 1):
        bgra = cv.cvtColor(arr, cv.COLOR_GRAY2BGRA)
    elif len(arr.shape) == 3 and arr.shape[2] == 3:
        bgra = cv.cvtColor(arr, cv.COLOR_BGR2BGRA)
    else:
        bgra = arr
    image = QtGui.QImage(bgra.data, bgra.shape[1], bgra.shape[0], QtGui.QImage.Format_ARGB32)
    return QtGui.QPixmap.fromImage(image)


def pixmap_to_array(image):
    from PyQt4 import QtGui
    if not isinstance(image, QtGui.QImage):
        image = QtGui.QImage(image)

    assert isinstance(image, QtGui.QImage)

    image = image.convertToFormat(QtGui.QImage.Format_ARGB32)

    width = image.width()
    height = image.height()

    ptr = image.constBits()
    ptr.setsize(image.byteCount())

    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    return arr[..., :3].copy()


def pil_image_to_array(img):
    img = np.array(img)
    return img[:, :, ::-1].copy()


def fit_to_size(image, size, position="center", background=0, interpolation=None):
    size = (int(size[0]), int(size[1]))

    if len(image.shape) == 2:
        shape = (size[1], size[0])
    else:
        shape = (size[1], size[0], image.shape[-1])

    im_height, im_width = image.shape[:2]
    w, h = size

    if 1.*im_height/im_width >= 1.*h/w:
        # original image taller - resizing to fit height
        oh = h
        ow = int(1.*im_width*h/im_height)
    else:
        # original image wider - resizing to fit width
        ow = w
        oh = int(1. * im_height * w / im_width)

    ow = max(ow, 1)
    oh = max(oh, 1)

    if interpolation is None:
        if w > im_width and h > im_height: 
            interpolation = cv.INTER_LINEAR
        else: 
            interpolation = cv.INTER_AREA

    out = np.full(shape, background, image.dtype)
    image = cv.resize(image, (ow, oh), interpolation=interpolation)

    if position == "center":
        x = w//2-ow//2
        y = h//2-oh//2
    else:
        x = y = 0

    out[y:y+oh, x:x+ow, ...] = image
    return out
