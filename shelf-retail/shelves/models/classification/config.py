import json
from hopt import Parameters, randoms

from shelves.models.classification.generators import MealsClassifierTestDataGenerator, MealsClassifierBatchGenerator, MealsClassifierValDataGenerator
from vision.config.auto import *


@auto_config
class config(config):
    class base:
        model_name = "nasnet"
        verbose_level = 1
        gpus = 1
        input = (224, 224, 3)
        lock_first_layers = 0.0

    class meals_multilabel(base):
        out_name = "resnext"
        version_dir = "v_tmp"

        logging_path = "/tytan/raid/shelf-retail/models/classification/{}/{}".format(out_name, version_dir)
        checkpoint_path = "/tytan/raid/shelf-retail/models/classification/{}/{}".format(out_name, version_dir)
        checkpoint_interval = 1

        input = (224, 224, 3)
        model_name = "resnext"
        metrics = ["whole_accuracy"]
        loss_func = "binary_crossentropy_with_threshold"
        last_activation = "sigmoid"

        steps_per_epoch = 100
        mapping_path = "/tytan/raid/shelf-retail/data/classification/mapping.json"

        generator = MealsClassifierBatchGenerator
        val_generator = MealsClassifierBatchGenerator
        test_generator = MealsClassifierTestDataGenerator
        testval_generator = MealsClassifierValDataGenerator
        generator_params = {
            "pad_image": True,
            "multilabel": True,
            "use_unknown_class": True,
            "mapping_path": mapping_path,
            "max_validation_size": 1000,
        }

        data_path = ["/tytan/raid/shelf-retail/data/classification/v05/train/labels.json",
                     "/tytan/raid/shelf-retail/data/classification/aug/v02/train/labels.json"]
        with open(mapping_path, "r") as f:
            class_names = list(json.load(f).keys())
        number_of_class = len(class_names)
        train_batch_size = 8

        use_validation = True
        val_data_path = ["/tytan/raid/shelf-retail/data/classification/v05/val/labels.json",
                         "/tytan/raid/shelf-retail/data/classification/aug/v02/val/labels.json"]
        val_batch_size = train_batch_size
        validation_steps = 50

        test_data_path = "/tytan/raid/shelf-retail/data/classification/v05/test/labels.json"
        test_batch_size = 4
        test_steps = None

        monitoring_measure = "val_loss"
        # params' values found in hyperparam search
        optimizer = "adam"
        lr = 0.0004
        decay = 0.1
        epochs = 1000
        weights = "imagenet"

        early_stopping_min_delta = 1e-6
        early_stopping_patience = 500

    class meals_multilabel_hyperparam_search(meals_multilabel, Parameters):
        out_name = "resnext"
        version_dir = "v_tmp"
        out_dir = "/tytan/raid/shelf-retail/models/classification/{}/{}".format(out_name, version_dir)
        lr = randoms.FloatChoice([0.010, 0.0004])
        train_batch_size = randoms.IntChoice([8, 16])
        decay = randoms.FloatChoice([0.0001, 0.01])
        optimizer = randoms.StrChoice(["nadam", "adam", "rmsprop"])
        epochs = 30
        search_iter = 100
        steps_per_epoch = 100
