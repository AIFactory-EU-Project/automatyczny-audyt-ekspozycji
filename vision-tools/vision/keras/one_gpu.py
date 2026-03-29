from __future__ import print_function

import sys

if "keras" in sys.modules or "tensorflow" in sys.modules:
    raise ImportError("Cannot load keras/tensorflow before GPU assignment")

import os

if os.environ.get("CUDA_VISIBLE_DEVICES", None):
    print("Running CUDA on GPU:", os.environ["CUDA_VISIBLE_DEVICES"])
else:
    from vision.helpers.gpu import free_gpu

    selected_gpu = free_gpu(11000, 90)

    os.environ["CUDA_VISIBLE_DEVICES"] = str(selected_gpu.uuid)
    # os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    print("Running CUDA on GPU:", selected_gpu)
