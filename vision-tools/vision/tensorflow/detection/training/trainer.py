"""
Helper for running object detection training and evaluation processes
"""

import os
import subprocess
import atexit
import functools
import time
import datetime
from string import Template
import shutil


class Trainer:

    FASTER_RCNN_INCEPTION_RESNET_V2 = 0
    FASTER_RCNN_NAS = 1
    SSD_MOBILENET = 2
    SSD_RESNET50 = 3
    SSD_INCEPTION_V2 = 4
    RFCN_RESNET101 = 5

    def __init__(self, directory, training_id, training_memory_fraction, save_interval_secs):
        self.directory = directory
        self.training_id = training_id
        self.training_directory = os.path.join(self.directory,
                                               "{0}_{1}".format(self.training_id,
                                                                datetime.datetime.now().strftime("%d-%m_%H:%M")))
        self.training_memory_fraction = training_memory_fraction
        self.save_interval_secs = save_interval_secs
        self.config_path = None

        self.train_script_path, self.eval_script_path = self.get_paths()

        if not os.path.exists(self.training_directory):
            os.makedirs(self.training_directory)

    @staticmethod
    def get_paths():
        import object_detection
        train_script_path = os.path.abspath(object_detection.__file__).replace("__init__.py", "train.py")
        eval_script_path = os.path.abspath(object_detection.__file__).replace("__init__.py", "eval.py")
        return train_script_path, eval_script_path

    @staticmethod
    def get_template(net_type):
        template_map = {Trainer.FASTER_RCNN_INCEPTION_RESNET_V2: os.path.join(os.path.dirname(__file__), "config", "faster_rcnn_inception_resnet_v2_template.config"),
                        Trainer.FASTER_RCNN_NAS: os.path.join(os.path.dirname(__file__), "config", "faster_rcnn_nas_template.config"),
                        Trainer.SSD_MOBILENET: os.path.join(os.path.dirname(__file__), "config", "ssd_mobilenet_v1_coco.config"),
                        Trainer.SSD_RESNET50: os.path.join(os.path.dirname(__file__), "config", "ssd_resnet50_v1_fpn_shared_box_predictor_640x640_coco14_sync.conifg"),
                        Trainer.SSD_INCEPTION_V2: os.path.join(os.path.dirname(__file__), "config", "ssd_inception_v2_coco.config"),
                        Trainer.RFCN_RESNET101: os.path.join(os.path.dirname(__file__), "config", "rfcn_resnet101_coco.config")}

        assert net_type in template_map.keys(), "No template for net_type {}".format(net_type)
        return template_map.get(net_type)

    @staticmethod
    def get_default_checkpoint(net_type):
        checkpoint_map = {Trainer.FASTER_RCNN_INCEPTION_RESNET_V2: "/tytan/raid/tf-detection-models/faster_rcnn_inception_resnet_v2_atrous_coco_2018_01_28/model.ckpt",
                          Trainer.FASTER_RCNN_NAS: "/tytan/raid/tf-detection-models/faster_rcnn_nas_coco_2018_01_28/model.ckpt",
                          Trainer.SSD_MOBILENET: "/tytan/raid/tf-detection-models/ssd_mobilenet_v1_coco_2018_01_28/model.ckpt",
                          Trainer.SSD_RESNET50: "/tytan/raid/tf-detection-models/ssd_resnet50_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03/model.ckpt",
                          Trainer.SSD_INCEPTION_V2: "/tytan/raid/tf-detection-models/ssd_inception_v2_coco_2018_01_28/model.ckpt",
                          Trainer.RFCN_RESNET101: "/tytan/raid/tf-detection-models/rfcn_resnet101_coco_2018_01_28/model.ckpt"}

        assert net_type in checkpoint_map.keys(), "No default checkpoint for net_type {}".format(net_type)
        return checkpoint_map.get(net_type)

    def save_training_script(self, script_path):
        shutil.copy(script_path, self.training_directory)

    def set_config(self,
                   net_type,
                   number_of_classes,
                   training_tfrecords_path,
                   evaluation_tfrecords_path,
                   label_map_path,
                   non_max_suppression_iou_threshold=0.6,
                   initial_checkpoint=None,
                   max_detections_per_class=100,
                   max_total_detections=100,
                   use_best_saver_eval=False,
                   saver_metric_eval="precision"):

        config_template_path = Trainer.get_template(net_type)
        if initial_checkpoint is None:
            initial_checkpoint = Trainer.get_default_checkpoint(net_type)

        pipeline_config = {"number_of_classes": number_of_classes,
                           "training_tfrecords_path": "".join(["\"", training_tfrecords_path, "\""]),
                           "evaluation_tfrecords_path": "".join(["\"", evaluation_tfrecords_path, "\""]),
                           "label_map_path": "".join(["\"", label_map_path, "\""]),
                           "initial_checkpoint": "".join(["\"", initial_checkpoint, "\""]),
                           "non_max_suppression_iou_threshold": non_max_suppression_iou_threshold,
                           "max_detections_per_class": max_detections_per_class,
                           "max_total_detections": max_total_detections,
                           "use_best_saver_eval": use_best_saver_eval,
                           "saver_metric_eval": saver_metric_eval
                           }

        with open(config_template_path) as config_template:
            source = Template(config_template.read())
        result = source.substitute(pipeline_config)

        self.config_path = os.path.join(self.training_directory, "training.config")
        with open(self.config_path, "w") as pipeline_config:
            pipeline_config.write(result)
        shutil.copy(label_map_path, self.training_directory)

    def get_commands(self):
        train_dir = os.path.join(self.training_directory, "train")
        eval_dir = os.path.join(self.training_directory, "eval")
        train_cmd = "python {0} --logtostderr " \
                    "--pipeline_config_path={1} " \
                    "--train_dir={2} " \
                    "--gpu_memory_fraction={3} " \
                    "--save_interval_secs={4}".format(self.train_script_path, self.config_path, train_dir,
                                                      self.training_memory_fraction, self.save_interval_secs)
        eval_cmd = "python {0} --logtostderr " \
                   "--pipeline_config_path={1} " \
                   "--checkpoint_dir={2} " \
                   "--eval_dir={3}".format(self.eval_script_path, self.config_path, train_dir, eval_dir)

        return train_cmd, eval_cmd

    def run(self):
        train_cmd, eval_cmd = self.get_commands()
        print("Running train and eval commands:\n{0}\n{1}".format(train_cmd, eval_cmd))
        print("## Starting Training process")
        p_train = subprocess.Popen(train_cmd.split())
        time.sleep(150)
        print("## Starting Evaluation process")
        p_eval = subprocess.Popen(eval_cmd.split())

        cleanup = functools.partial(self.__cleanup, [p_train, p_eval])
        atexit.register(cleanup)

        subprocess.Popen.wait(p_train)

    @staticmethod
    def __cleanup(processes):
        for p in processes:
            try:
                subprocess.Popen.terminate(p)
            except OSError:
                pass


def main():
    """ Example usage taken from drugs-counter project"""
    from vision.tensorflow import gpus

    directory = "/tytan/raid/drugs-counter/trainings/tabcin_gripex"
    training_id = "detection_original"
    training_memory_fraction = 0.75
    save_interval_secs = 900

    trainer = Trainer(directory, training_id, training_memory_fraction, save_interval_secs)

    number_of_classes = 4
    training_tfrecords_path = "/tytan/raid/drugs-counter/datasets/tabcin_gripex/original/train/tfrecords/detection_train.record"
    evaluation_tfrecords_path = "/tytan/raid/drugs-counter/datasets/tabcin_gripex/original/val/tfrecords/detection_val.record"
    label_map_path = "/tytan/raid/drugs-counter/data/tabcin_gripex/detection_label_map.pbtxt"

    trainer.set_config(Trainer.FASTER_RCNN_INCEPTION_RESNET_V2,
                       number_of_classes,
                       training_tfrecords_path,
                       evaluation_tfrecords_path,
                       label_map_path,
                       use_best_saver_eval=True)

    trainer.save_training_script(__file__)

    gpus.tensorflow_use_gpus(1)
    trainer.run()
