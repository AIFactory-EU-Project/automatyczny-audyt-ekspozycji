import aug


# TODO: need to tweak params
class OcrPipeline(aug.Pipeline):
    def __init__(self):
        self.ops = aug.Sequential(
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
                                       orientation="horizontal"),
                    aug.LinearGradient(p=1., edge_brightness=(aug.uniform(.0, .05),
                                                              aug.uniform(.1, .4)),
                                       orientation="vertical")
                ),
            ),

            aug.GaussNoise(p=.5, avg=0, std_dev=aug.uniform(6, 15)),
            aug.SaltNoise(p=.2, percent=aug.uniform(0.0001, 0.0008)),
            aug.PepperNoise(p=.2, percent=aug.uniform(0.0001, 0.0008)),
            aug.JpegNoise(p=.4, quality=aug.uniform(.1, .5)),
            aug.Blurs(p=.5),
            aug.Pixelize(p=.4, ratio=aug.uniform(.65, 1.)),
            aug.Zoom(p=.5, margin=aug.uniform(0.01, 0.05)),
        )

    def apply(self, sample):
        return self.ops.apply(sample)
