import aug

import ocr.aug.transformations.ops as aug_custom


class EmbossedCompositePipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.Stretch(p=.7, x_scale=aug.uniform(.0, .45), y_scale=aug.uniform(.0, .45)),
            aug.GaussNoise(p=.7, std_dev=20),
            aug.SaltNoise(p=.8, percent=aug.uniform(.0001, .0007)),
            aug.PepperNoise(p=.8, percent=aug.uniform(.0001, .0007)),
            aug.RandomRadialDirt(p=.5),
            aug.Choice(
                aug.AddBrightness(p=.6, value=aug.uniform(5, 15), dev=6),
                aug.AddDarkness(p=.7, value=aug.uniform(5, 70), dev=6),
                aug.AddDarkness(p=.05, value=aug.uniform(70, 110), dev=15)
            ),
            aug.RadialGradient(p=.7, inner_color=aug.uniform(16, 40), outer_color=aug.uniform(0, 15)),
            aug.Pixelize(p=.8, ratio=aug.uniform(1., 4.)),
            aug.Choice(
                aug.GaussianBlur(p=.9, ksize_norm=aug.uniform(.02, .15), sigma=aug.uniform(1, 5), direction="horizontal"),
                aug.GaussianBlur(p=.9, ksize_norm=aug.uniform(.02, .15), sigma=aug.uniform(1, 5), direction="vertical"),
                aug.GaussianBlur(p=.9, ksize_norm=aug.uniform(.02, .15), sigma=aug.uniform(1, 5))
            ),
            aug.Choice(
                aug.HorizontalCut(p=.45, left=aug.uniform(.0, .09), right=aug.uniform(.0, .09), rescale=False),
                aug.VerticalCut(p=.45, top=aug.uniform(.0, .14), bottom=aug.uniform(.0, .14), rescale=False)
            )
        )

    def apply(self, sample):
        return self.ops.apply(sample)


class EmbossedTextPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.Rotation(p=.8, angle=aug.uniform(-5, 5), border_value=[255, 255, 255, 0]),
            # simulate eroded text
            aug.RandomCurveContour(p=.8, color=[255, 255, 255, 0], limit=aug.uniform(1000, 5000), iterations=aug.uniform(1, 5)),
            # draw random black contours
            aug.RandomCurveContour(p=.3, color=aug.uniform([0, 0, 0, 0], [50, 50, 50, 255]), limit=aug.uniform(500, 1500), iterations=aug.uniform(1, 4)),
            aug.RandomSizeBorder(p=.8, horizontal_sides_probability=.7, vertical_sides_probability=.6, max_border=aug.uniform(.0, .3)),
            aug_custom.OcrDrawCutCharacters(p=.7)
        )

    def apply(self, sample):
        return self.ops.apply(sample)
