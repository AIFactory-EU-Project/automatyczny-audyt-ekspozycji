import aug


class FrontFaceCompositePipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.Stretch(p=1., x_scale=.25, y_scale=.25),
            aug.Choice(
                aug.LinearGradient(p=1., orientation="horizontal"),
                aug.LinearGradient(p=1., orientation="vertical")
            ),
            aug.Choice(
                aug.AddBrightness(p=1., value=aug.uniform(0, 30)),
                aug.AddDarkness(p=1., value=aug.uniform(40, 80)),
                aug.AddDarkness(p=1., value=aug.uniform(10, 80))
            ),
            aug.Pixelize(p=1., ratio=aug.uniform(1., 2.)),
            aug.GaussianBlur(p=.5, ksize_norm=aug.uniform(.02, .15), sigma=aug.uniform(0, 3))
        )

    def apply(self, sample):
        return self.ops.apply(sample)


class FrontFaceForegroundPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.RandomRadialDirt(p=.2),
            aug.GaussNoise(p=.7),
            aug.GaussianBlur(p=.5, ksize_norm=aug.uniform(.02, .15), sigma=aug.uniform(0, 3))
        )

    def apply(self, sample):
        return self.ops.apply(sample)
