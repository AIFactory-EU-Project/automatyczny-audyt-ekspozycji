from __future__ import print_function

import sys

if "keras" in sys.modules or "tensorflow" in sys.modules:
    raise ImportError("Cannot load keras/tensorflow before GPU assignment")

import os

if os.environ.get("CUDA_VISIBLE_DEVICES", None):
    print("Running CUDA on GPU:", os.environ["CUDA_VISIBLE_DEVICES"])
else:

    from vision.helpers.gpu import free_gpus

    selected_gpus = free_gpus(11000, 90)
    selected_gpus = ",".join([str(gpu.uuid) for gpu in selected_gpus])

    os.environ["CUDA_VISIBLE_DEVICES"] = selected_gpus
    print("Running CUDA on GPU:", selected_gpus)
