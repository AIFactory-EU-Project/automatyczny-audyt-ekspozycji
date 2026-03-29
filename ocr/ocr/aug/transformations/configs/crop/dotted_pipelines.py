import aug

import ocr.aug.transformations.ops as aug_custom


class DottedBackgroundPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.AdjustDarkness(p=1.),
            aug.RandomEdge(p=.2)
        )

    def apply(self, sample):
        return self.ops.apply(sample)


class DottedCompositePipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.Stretch(p=.7, x_scale=aug.uniform(.0, .45), y_scale=aug.uniform(.0, .45)),
            aug.GaussNoise(p=.7, std_dev=15),
            aug.SaltNoise(p=.8, percent=aug.uniform(.0001, .0007)),
            aug.PepperNoise(p=.8, percent=aug.uniform(.0001, .0007)),
            aug.RandomRadialDirt(p=.1),
            aug.Choice(
                aug.AddBrightness(p=.6, value=aug.uniform(5, 20)),
                aug.AddDarkness(p=.7, value=aug.uniform(5, 70)),
                aug.AddDarkness(p=.05, value=aug.uniform(70, 110), dev=15)
            ),
            aug.RadialGradient(p=.7, inner_color=aug.uniform(90, 110), outer_color=aug.uniform(0, 30)),
            aug.Pixelize(p=.8, ratio=aug.uniform(1., 4.)),
            aug.Choice(
                aug.GaussianBlur(p=.9, ksize_norm=aug.uniform(.02, .15), sigma=aug.uniform(1, 5), direction="horizontal"),
                aug.GaussianBlur(p=.9, ksize_norm=aug.uniform(.02, .15), sigma=aug.uniform(1, 5), direction="vertical"),
                aug.GaussianBlur(p=.9, ksize_norm=aug.uniform(.02, .15), sigma=aug.uniform(1, 5))
            ),
            aug.Choice(
                aug.HorizontalCut(p=.45, left=aug.uniform(.0, .065), right=aug.uniform(.0, .065), rescale=False),
                aug.VerticalCut(p=.45, top=aug.uniform(.0, .065), bottom=aug.uniform(.0, .065), rescale=False)
            )
        )

    def apply(self, sample):
        return self.ops.apply(sample)


class DottedTextPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.Rotation(p=.8, angle=aug.uniform(-4, 4), border_value=[255, 255, 255, 0]),
            aug.RandomSizeBorder(p=.8, horizontal_sides_probability=.7, vertical_sides_probability=.6, max_border=aug.uniform(.0, .3)),
            # simulate eroded text
            aug.RandomCurveContour(p=.7, color=[255, 255, 255, 0], limit=aug.uniform(1000, 2000)),
            # draw random colorful contours
            aug.RandomCurveContour(p=.3, color=aug.uniform([0, 0, 0, 50], [255, 255, 255, 150]), limit=aug.uniform(400, 1500), iterations=aug.uniform(1, 4)),
            # draw random gray contours
            aug.RandomCurveContour(p=.3, color=aug.uniform([0, 0, 0, 50], [50, 50, 50, 300]), limit=aug.uniform(400, 1500), iterations=aug.uniform(1, 4)),
            aug_custom.OcrDrawCutCharacters(p=.7),
            aug_custom.OcrTemplateContour(p=.05)
        )

    def apply(self, sample):
        return self.ops.apply(sample)
