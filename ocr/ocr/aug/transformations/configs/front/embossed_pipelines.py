import aug


class EmbossedTextPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
            aug.Rotation(p=1., angle=aug.uniform(-3, 3), border_value=[255, 255, 255, 0])
        )

    def apply(self, sample):
        return self.ops.apply(sample)
