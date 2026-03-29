from __future__ import print_function

import sys

if "keras" in sys.modules or "tensorflow" in sys.modules:
    raise ImportError("Cannot load keras/tensorflow before GPU assignment")

import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
