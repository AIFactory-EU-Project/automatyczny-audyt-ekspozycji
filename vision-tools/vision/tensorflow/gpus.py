import os
import sys

from vision.helpers.gpu import free_gpus


def tensorflow_use_gpus(number, required_memory=0, required_usage=0, memory_limit_fraction=1.0, take_all_memory=False):
    selected_gpus = [-1]
    if number > 0:
        selected_gpus = list(free_gpus(required_memory, required_usage))[:number]
        if not selected_gpus:
            raise Exception("There are no free GPUs!")

        selected_gpus = [gpu.uuid for gpu in selected_gpus]
    tensorflow_use_specific_gpus(selected_gpus, memory_limit_fraction, take_all_memory)


def tensorflow_use_specific_gpus(gpu_list, memory_limit_fraction=1.0, take_all_memory=False):
    if "keras" in sys.modules or "tensorflow" in sys.modules:
        raise ImportError("Cannot load keras/tensorflow before GPU assignment")

    selected_gpus = ",".join([str(g) for g in gpu_list])

    os.environ["CUDA_VISIBLE_DEVICES"] = selected_gpus
    print("Running tensorflow on GPU", selected_gpus)

    import tensorflow as tf

    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = memory_limit_fraction
    config.gpu_options.allow_growth = not take_all_memory
    tf.Session(config=config).as_default()
