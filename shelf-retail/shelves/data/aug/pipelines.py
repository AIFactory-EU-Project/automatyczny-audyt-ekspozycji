import numpy as np
import cv2

import aug
from aug import Operation


@aug.perform_randomly
class NormalizeSize(Operation):
    def __init__(self, max_dimension):
        self._max_dimension = max_dimension
        self._ratio = None

    def apply_on_image(self, image):
        current_max_dim = np.max(image.shape[:2])
        if current_max_dim > self._max_dimension:
            ratio = 1.0 * self._max_dimension / current_max_dim
            self._ratio = ratio
            resized = cv2.resize(image, None, fx=ratio, fy=ratio)
            return resized
        else:
            return image


class ClassificationPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            NormalizeSize(p=1., max_dimension=300),
            aug.Choice(
                aug.Contrast(p=.5, scale=aug.uniform(.3, 1.7)),
                aug.GlobalBrightness(p=.5, change=aug.uniform(.02, .98))
            ),
            aug.Choice(
                aug.RadialGradient(p=.25,
                                   inner_color=aug.uniform(160, 200),
                                   outer_color=aug.uniform(0, 10),
                                   random_distance=True),
                aug.Choice(
                    aug.LinearGradient(p=1., edge_brightness=(aug.uniform(.0, .05),
                                                              aug.uniform(.1, .4)),
                                       orientation='horizontal'),
                    aug.LinearGradient(p=1., edge_brightness=(aug.uniform(.0, .05),
                                                              aug.uniform(.1, .4)),
                                       orientation='vertical')
                ),
            ),
            aug.Zoom(p=0.5),
            aug.GaussNoise(p=.5, avg=0, std_dev=aug.uniform(6, 15)),
            aug.SaltNoise(p=.2, percent=aug.uniform(0.0001, 0.0008)),
            aug.PepperNoise(p=.2, percent=aug.uniform(0.0001, 0.0008)),
            aug.CutOut(p=.1, size_range=(.02, .03), iterations=aug.uniform(1, 4)),
            aug.JpegNoise(p=.4, quality=aug.uniform(.1, .5)),
            aug.Blurs(p=.5),
            aug.Pixelize(p=.4, ratio=aug.uniform(.65, 1.)),
            aug.Zoom(p=.5, margin=aug.uniform(0.01, 0.05)),
            aug.Rotation(p=.4, angle=aug.uniform(-7, 7)),
            aug.PerspectiveTransformation(p=.3, max_warp=aug.uniform(.1, .2))
        )

    def apply(self, sample):
        return self.ops.apply(sample)
