from ..default import *


@apply_config
class config(config):
    class paths(config.paths):
        pass

    class caffe(config.caffe):
        default_home = '/home/?????????USERNAME???????/caffe/python'
        default_gpu = 0
