import os
import glob
import object_detection
from vision.tensorflow.gpus import tensorflow_use_gpus


def export_graph(model_home_dir):
    assert os.path.isdir(model_home_dir), "Please set correct path before running script"

    ckpt_name = "best" if "eval" in model_home_dir else "model"
    checkpoint_paths = glob.glob(os.path.join(model_home_dir, "{}.ckpt-*.meta".format(ckpt_name)))
    checkpoint_path = max(checkpoint_paths).replace(".meta", "")
    pipeline_config_path = os.path.join(model_home_dir, "pipeline.config")
    output_path = os.path.join(os.path.dirname(model_home_dir), "exported_model")
    export_script_path = os.path.abspath(object_detection.__file__).replace("__init__.py", "export_inference_graph.py")

    command = ("python {export_script_path} "
               "--input_type image_tensor "
               "--pipeline_config_path {pipeline_config_path} "
               "--trained_checkpoint_prefix {checkpoint_path} "
               "--output_directory {output_path}".format(**locals()))

    print("Running {0}".format(command))
    tensorflow_use_gpus(1)
    os.system(command)
