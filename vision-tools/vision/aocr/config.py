from __future__ import absolute_import

import json
import logging
from datetime import datetime
import os
from importlib import import_module
import six
import yaml

from vision.aocr.random_params import IntParam, FloatParam, BaseParam
from vision.config.config import all_vars
from vision.config.auto import apply_config, config, Config


logging.basicConfig(level=logging.DEBUG, format="%(levelname).1s %(message)s")


@apply_config
class config(config):
    class aocr(Config):
        class base(Config):
            """Base class for the whole AOCR thing ;)"""

            home_dir = "/kolos/m2/ocr"  # base dir of everything ;)

            data_dir = "{home_dir}/data"  # base dir for data source
            training_dir = "{home_dir}/aocr/training"  # base dir where training will take place

            output_dir = "{training_dir}/aocr-output"  # temporary output directory
            dataset_path = "{training_dir}/{name}/data"  # dir where TFRecords will be created
            model_dir = "{training_dir}/{name}"  # dir where models and checkpoints will be saved

            checkpoint = 0  # number or path to the checkpoint to load (can be used with load() function)

            name = "unknown-name"  # name for the whole training
            load_model = True  # if False, reset the net to random weights

            # ANN parameters

            max_width = 256  # width of the input image
            max_height = 32  # height of the input image
            channels = 3  # number of channels of the input image

            max_prediction = 15  # max length of predicted string
            char_map = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"  # characters to be recognized
            char_subst = {"": ""}  # character substitutions. "" means "all other"
            uppercase = True  # convert everything to upper case

            return_raw = False  # shall the net also return raw outputs
            custom_confidence = None  # return custom confidence (calculated from raw outputs)  default: (0, 20)

            # datasets (generators!)
            data_train = lambda: []
            data_test = lambda: []
            data_val = lambda: []

            # training parameters
            batch_size = 400
            num_epoch = 100
            steps_per_checkpoint = 500
            steps_per_test = 500

            # hyperparameters
            initial_learning_rate = 1

            target_embedding_size = 50
            attn_num_hidden = 150
            attn_num_layers = 2
            clip_gradients = True
            max_gradient_norm = 3.0
            dropout = 0.5
            reg_val = 0

            # other options
            gpu_id = 0
            use_gru = False  # GRU instead of LSTM
            use_distance = True  # Levenshtein distance

            # visualization options - used in model.test() function
            visualize = False
            show_correct = False
            show_incorrect = False
            show_raw = False

            @classmethod
            def instance(cls):
                """Creates an instance of config for random search (instantiates hyperparameters)"""

                class cls(cls):
                    run = "run-" + datetime.now().strftime("%Y%m%d-%H%M%S")
                    model_dir = cls.model_dir

                    if "[run]" in model_dir:
                        model_dir = model_dir.replace("[run]","{run}")

                    if "{run}" in model_dir:
                        model_dir = model_dir.format(run=run)

                for attr_name in all_vars(cls):
                    attr = getattr(cls, attr_name)
                    if isinstance(attr, BaseParam):
                        setattr(cls, attr_name, attr.get())

                return cls

            @classmethod
            def save(cls):
                """Saves this config to {model_dir}/config.json and {model_dir}/config.yaml"""
                data = cls.asdict()
                data = {k: v for k, v in six.iteritems(data) if not callable(v)}

                with open(cls.model_dir + "/config.json", "w") as f:
                    json.dump(data, f, indent=4, sort_keys=True)

                with open(cls.model_dir + "/config.yaml", "w") as f:
                    yaml.dump(data, f)

            @classmethod
            def load(cls):
                """Loads this config from checkpoint (if provided) and {model_dir}/config.json"""
                checkpoint = cls.checkpoint
                if checkpoint:
                    cls.model_dir = os.path.dirname(checkpoint)

                with open(cls.model_dir + "/config.json") as f:
                    data = json.load(f)

                for k, v in six.iteritems(data):
                    setattr(cls, k, v)

                if checkpoint:
                    cls.checkpoint = checkpoint

        class search(base):
            """Base class for random hyperparameter search"""
            name = "search-hyperparams"
            run = "unknown-run"

            dataset_path = "{training_dir}/{name}/data"
            model_dir = "{training_dir}/{name}/{{run}}"

            num_epoch = 40
            processes = 4

            target_embedding_size = IntParam(5, 50)  # default: 10
            attn_num_hidden = IntParam(16, 256)  # default: 128
            attn_num_layers = IntParam(2,2)  # default: 2
            max_gradient_norm = FloatParam(1, 10)  # default: 5.0
            dropout = FloatParam(0, 0.8)  # default: 0.5


def load_config_from_checkpoint(checkpoint):
    c = config.aocr.base.instance()
    c.checkpoint = checkpoint
    c.load()
    return c


def load_config(config):
    if isinstance(config, six.string_types):
        pos = config.rindex(".config.")
        module_name = config[:pos]
        class_name = config[pos+1:].split(".")
        config = import_module(module_name)
        for name in class_name:
            config = getattr(config, name)

    return config
