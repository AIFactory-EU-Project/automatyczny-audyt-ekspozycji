import random
import cv2
import numpy as np

from aug import Operation, perform_randomly


class RotationWithBound(Operation):

    def __init__(self,
                 angle,
                 interpolation=cv2.INTER_LINEAR,
                 mode=cv2.BORDER_CONSTANT,
                 border_value=(255, 255, 255),
                 change_size=True):
        self._angle = angle
        self._interpolation = interpolation
        self._mode = mode
        self._border_value = border_value
        self._change_size = change_size
        self.mtx = None
        self.new_width = None
        self.new_height = None

    def apply_on_image(self, image):
        im_height, im_width = image.shape[:2]
        if self._change_size:
            center_x, center_y = im_width // 2, im_height // 2

            if self.mtx is None:
                self.mtx = cv2.getRotationMatrix2D((center_x, center_y), self._angle, 1.0)
                cos = np.abs(self.mtx[0, 0])
                sin = np.abs(self.mtx[0, 1])

                self.new_width = int((im_height * sin) + (im_width * cos))
                self.new_height = int((im_height * cos) + (im_width * sin))

                # Adjust rotation matrix to take translation into account
                self.mtx[0, 2] += (self.new_width / 2) - center_x
                self.mtx[1, 2] += (self.new_height / 2) - center_y

            return cv2.warpAffine(image,
                                  self.mtx, (self.new_width, self.new_height),
                                  flags=self._interpolation,
                                  borderMode=self._mode,
                                  borderValue=self._border_value)

        if self.mtx is None:
            self.mtx = cv2.getRotationMatrix2D((im_width / 2, im_height / 2), self._angle, 1.0)

        img = cv2.warpAffine(image,
                             self.mtx, (im_width, im_height),
                             flags=self._interpolation,
                             borderMode=self._mode,
                             borderValue=self._border_value)

        return img


@perform_randomly
class Rotation(Operation):

    def __init__(self, angle=30, border_value=None, mode='zeros'):
        self._angle = angle
        self._mode = mode
        self._border_value = border_value
        self._mtx = None

        self._w_ratio = 1.
        self._h_ratio = 1.

    def apply_on_image(self, image):
        im_height, im_width = image.shape[:2]

        if self._border_value is None:
            self._border_value = [0] * image.shape[2]

        if self._mode == "zeros":
            mode = cv2.BORDER_CONSTANT
        elif self._mode == "replicate":
            mode = cv2.BORDER_REPLICATE
        else:
            raise Exception("Unknown mode value.")

        rotation_with_bound = RotationWithBound(self._angle,
                                                border_value=self._border_value,
                                                mode=mode)

        image = rotation_with_bound.apply_on_image(image)
        self._mtx = rotation_with_bound.mtx

        tmp_h, tmp_w = image.shape[:2]
        self._w_ratio = tmp_w / im_width
        self._h_ratio = tmp_h / im_height

        return cv2.resize(image, (im_width, im_height), interpolation=cv2.INTER_CUBIC)

    def apply_on_annotations(self, annotations):
        if self._mtx is None:
            return annotations

        polygons = []
        for polygon in annotations:
            points = []
            for point in polygon:
                point = np.array([point[0], point[1], 1])
                rotated = np.dot(self._mtx, point.T).astype(int).tolist()
                points.append(rotated)
            polygons.append(points)
        rotated = np.array(polygons).astype(np.float32)
        rotated[:, :, 0] /= self._w_ratio
        rotated[:, :, 1] /= self._h_ratio

        return rotated.astype(np.int32)

    def apply_on_masks(self, masks):
        return np.array([self.apply_on_image(mask) for mask in list(masks)])


@perform_randomly
class Stretch(Operation):

    def __init__(self, x_scale=0.5, y_scale=0.5):
        assert x_scale > 0 and y_scale > 0
        self._x_scale = x_scale
        self._y_scale = y_scale
        self._ratios = (1., 1.)

    def apply_on_image(self, image):
        im_height, im_width = image.shape[:2]

        if random.getrandbits(1):
            x_ratio = 1 - self._x_scale
            new_w = x_ratio * im_width
            new_w, new_h = int(new_w), im_height
            self._ratios = (x_ratio, 1.)
        else:
            y_ratio = 1 - self._y_scale
            new_h = y_ratio * im_height
            new_w, new_h = im_width, int(new_h)
            self._ratios = (1., y_ratio)

        return cv2.resize(image, (new_w, new_h))
    
    def apply_on_annotations(self, annotations):
        x_ratio, y_ratio = self._ratios
        annotations = annotations.astype(np.float32)
        annotations[:, :, 0] *= x_ratio
        annotations[:, :, 1] *= y_ratio
        annotations = annotations.astype(np.int32)
        return annotations


@perform_randomly
class Rotation90(Operation):

    def __init__(self, iterations=None):
        self._iterations = iterations if iterations is not None else random.randint(0, 3)

    def apply_on_image(self, image):
        for _ in range(self._iterations):
            image = np.ascontiguousarray(np.rot90(image))
        return image


@perform_randomly
class VerticalFlip(Operation):

    def __init__(self):
        self._h = None

    def apply_on_image(self, img):
        self._h = img.shape[0]
        return np.ascontiguousarray(img[::-1, ...])

    def apply_on_annotations(self, annotations):
        if self._h is not None:
            annotations[:, :, 1] = self._h - annotations[:, :, 1]

        return annotations

    def apply_on_masks(self, masks):
        return np.array([self.apply_on_image(mask) for mask in list(masks)])


@perform_randomly
class HorizontalFlip(Operation):

    def __init__(self):
        self._w = None

    def apply_on_image(self, img):
        self._w = img.shape[1]
        return np.ascontiguousarray(img[:, ::-1, ...])

    def apply_on_annotations(self, annotations):
        if self._w is not None:
            annotations[:, :, 0] = self._w - annotations[:, :, 0]

        return annotations

    def apply_on_masks(self, masks):
        return np.array([self.apply_on_image(mask) for mask in list(masks)])


@perform_randomly
class Transposition(Operation):

    def apply_on_image(self, img):
        return img.transpose(1, 0, 2) if len(img.shape) > 2 else img.transpose(1, 0)


@perform_randomly
class Zoom(Operation):

    def __init__(self, margin=0.1):
        assert 0. < margin < .5

        self._margin = margin
        self._top = None
        self._left = None
        self._w_ratio = 1.
        self._h_ratio = 1.
        self._shape = None

    def apply_on_image(self, image):
        self._shape = h, w = image.shape[:2]
        h_abs_margin, w_abs_margin = int(h * self._margin), int(w * self._margin)

        if self._left is None:
            self._left = int(w * random.uniform(0, self._margin))
        right = w_abs_margin - self._left

        if self._top is None:
            self._top = int(h * random.uniform(0, self._margin))
        bottom = h_abs_margin - self._top

        image = image[self._top:h - bottom, self._left:w - right]

        tmp_h, tmp_w = image.shape[:2]
        self._w_ratio = tmp_w / w
        self._h_ratio = tmp_h / h

        return cv2.resize(image, (w, h))

    def apply_on_annotations(self, annotations):
        if self._left is not None and self._top is not None:
            annotations = annotations.astype(np.float32)
            annotations[:, :, 0] -= self._left
            annotations[:, :, 1] -= self._top
            annotations[:, :, 0] /= self._w_ratio
            annotations[:, :, 1] /= self._h_ratio
            annotations = annotations.astype(np.int32)
        return annotations

    def apply_on_masks(self, masks):
        return np.array([self.apply_on_image(mask) for mask in list(masks)])


@perform_randomly
class Translation(Operation):
    def __init__(self, translate_percent=None, translate_px=None, mode=cv2.BORDER_CONSTANT, border_value=(0, 0, 0)):
        assert (translate_percent and not translate_px) or (translate_px and not translate_percent)

        self._translate_x = 0
        self._translate_y = 0
        self._translate_percent = translate_percent
        self._translate_px = translate_px
        self._border_value = border_value
        self._mode = mode
        self._parse_param()

    def apply_on_image(self, image):
        im_height, im_width = image.shape[:2]
        if isinstance(self._translate_x, float):
            self._translate_x = int(np.round(self._translate_x * im_width))
        if isinstance(self._translate_y, float):
            self._translate_y = int(np.round(self._translate_y * im_height))

        translation_mtx = np.float32([[1, 0, self._translate_x], [0, 1, self._translate_y]])
        return cv2.warpAffine(image, translation_mtx, (im_width, im_height),
                              flags=cv2.INTER_LINEAR,
                              borderMode=self._mode,
                              borderValue=self._border_value)

    def apply_on_annotations(self, annotations):
        annotations[:, :, 0] += self._translate_x
        annotations[:, :, 1] += self._translate_y
        return annotations

    def _parse_param(self):
        def _parse_single_param(p):
            if isinstance(p, tuple):
                assert len(p) == 2
                a, b = p
                assert type(a) is type(b)
                p = int(random.uniform(a, b))
            assert (isinstance(p, float) and self._translate_percent) or (isinstance(p, int) and self._translate_px)
            return p

        param = self._translate_percent if self._translate_percent else self._translate_px
        if isinstance(param, dict):
            assert "x" in param or "y" in param
            self._translate_x = _parse_single_param(param.get("x", 0))
            self._translate_y = _parse_single_param(param.get("y", 0))
        else:
            self._translate_x = self._translate_y = _parse_single_param(param)


@perform_randomly
class Scaling(Operation):
    def __init__(self, scale):
        self._scale = scale
        self._resizer = Resize(scale=self._scale)

    def apply_on_image(self, image):
        return self._resizer.apply_on_image(image)

    def apply_on_annotations(self, annotations):
        return self._resizer.apply_on_annotations(annotations)


@perform_randomly
class Resize(Operation):
    def __init__(self, dsize=None, scale=None):
        assert (dsize and not scale) or (scale and not dsize)
        if dsize:
            assert dsize and isinstance(dsize, tuple)
        else:
            assert scale > 0 and isinstance(scale, float)

        self._dsize = dsize
        self._scale = scale
        self._original_size = None

    def apply_on_image(self, image):
        im_height, im_width = image.shape[:2]
        self._original_size = (im_width, im_height)

        if self._scale:
            d_height = int(np.round(self._scale * im_height))
            d_width = int(np.round(self._scale * im_width))
            self._dsize = (d_width, d_height)

        interpolation = cv2.INTER_AREA if im_height > self._dsize[0] or im_width > self._dsize[1] else cv2.INTER_LINEAR
        return cv2.resize(image, self._dsize, interpolation=interpolation)

    def apply_on_annotations(self, annotations):
        if self._scale:
            return annotations * self._scale
        else:
            scale_x = self._dsize[0] / self._original_size[0]
            scale_y = self._dsize[1] / self._original_size[1]
            annotations = annotations.astype(np.float)
            annotations[:, :, 0] *= scale_x
            annotations[:, :, 1] *= scale_y
            return annotations
