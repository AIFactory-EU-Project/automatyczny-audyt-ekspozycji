import aug


class PrintedBackgroundPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.AdjustDarkness(p=1.)
        )

    def apply(self, sample):
        return self.ops.apply(sample)


class PrintedCompositePipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.Stretch(p=1., x_scale=aug.uniform(.0, 0.2), y_scale=aug.uniform(.0, 0.2)),
            aug.GaussNoise(p=.95, std_dev=20),
            aug.SaltNoise(p=.8, percent=aug.uniform(.0001, .0007)),
            aug.PepperNoise(p=.8, percent=aug.uniform(.0001, .0007)),
            aug.RandomRadialDirt(p=.5),
            aug.Choice(
                aug.AddBrightness(p=.6, value=aug.uniform(5, 40), dev=15),
                aug.AddDarkness(p=.7, value=aug.uniform(5, 70), dev=15),
                aug.AddDarkness(p=.05, value=aug.uniform(70, 110), dev=15)
            ),
            aug.Choice(
                aug.RadialGradient(p=.9, inner_color=aug.uniform(40, 50), outer_color=aug.uniform(0, 10)),
                aug.LinearGradient(p=.9)
            ),
            aug.GaussianBlur(p=.9)
        )

    def apply(self, sample):
        return self.ops.apply(sample)


class PrintedTextPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.Rotation(p=1., angle=aug.uniform(-1, 1), border_value=[255, 255, 255, 0]),
            aug.Choice(
                aug.HorizontalCut(p=.45, left=aug.uniform(.0, .08), right=aug.uniform(.0, .08)),
                aug.VerticalCut(p=.45, top=aug.uniform(.0, .08), bottom=aug.uniform(.0, .08)),
                aug.RandomSizeBorder(p=.9, max_border=aug.uniform(.0, .12), horizontal_sides_probability=.5, vertical_sides_probability=.3)
            )
        )

    def apply(self, sample):
        return self.ops.apply(sample)
