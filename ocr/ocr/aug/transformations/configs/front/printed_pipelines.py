import aug


class PrintedBackgroundPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.AdjustDarkness(p=1.)
        )

    def apply(self, sample):
        return self.ops.apply(sample)


class PrintedTextPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.ScatterLetters(p=.8),
            aug.Rotation(p=1., angle=aug.uniform(-3, 3), border_value=[255, 255, 255, 0])
        )

    def apply(self, sample):
        return self.ops.apply(sample)
