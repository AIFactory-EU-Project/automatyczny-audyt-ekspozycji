from __future__ import print_function

import os
from vision.helpers.gpu import free_gpu


def select_gpu(memory=11000, usage=90):
    selected_gpu = free_gpu(memory, usage)
    os.environ["CUDA_VISIBLE_DEVICES"] = str(selected_gpu.uuid)
    print("Running CUDA on GPU:", selected_gpu)
