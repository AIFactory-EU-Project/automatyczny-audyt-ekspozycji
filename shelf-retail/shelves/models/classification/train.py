import json
import numpy as np
import os
import sys
from datetime import datetime
from glob import glob
from pprint import pprint

from vision.metrics.numpy import multilabel
from vision.metrics.numpy.multilabel import f1score_spec
from vision.tensorflow.gpus import tensorflow_use_gpus


def train_model(train_config):
    from vision.config.config import all_vars
    from vision.keras.train import train as train_utils
    from vision.keras.train import logger

    datetime_str = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dir_path = train_utils.create_dir_for_training(train_config.logging_path, datetime_str)
    # log to screen and file
    output = logger.Logger(os.path.join(dir_path, "log.log"))
    sys.stdout = output

    # print configuration
    pprint(all_vars(train_config))

    # data generators
    g, validation_data, test_g = get_data_generators(train_config)
    validation_steps = train_config.validation_steps if train_config.use_validation else None

    # model
    model = get_model(train_config)
    metrics_names = getattr(train_config, "metrics", [])
    metrics = train_utils.get_metrics(metrics_names)
    loss = train_utils.get_loss(train_config.loss_func)
    optimizer = get_optimizer(train_config)
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    # callbacks
    callbacks = get_callbacks(train_config, test_g, dir_path, datetime_str)

    # training
    model.fit_generator(
        generator=g.next(),
        steps_per_epoch=train_config.steps_per_epoch,
        epochs=train_config.epochs,
        verbose=train_config.verbose_level,
        callbacks=callbacks,
        validation_data=validation_data,
        validation_steps=validation_steps,
        shuffle=False)


def get_data_generators(train_config):
    from vision.keras.train import generator
    gen_params = getattr(train_config, "generator_params", {})

    # Train generator
    g = generator.Generator(
        batch_generator=train_config.generator,
        data_file=train_config.data_path,
        batch_size=train_config.train_batch_size,
        input_size=train_config.input[:2],
        classes_no=train_config.number_of_class,
        **gen_params)

    # Test generator
    test_g = train_config.test_generator(
        data_file=train_config.test_data_path,
        batch_size=train_config.test_batch_size,
        input_size=train_config.input[:2],
        classes_no=train_config.number_of_class,
        **gen_params)
    test_g.name = "test"

    if train_config.use_validation:
        # Val generator
        val_g = generator.Generator(
            batch_generator=train_config.val_generator,
            data_file=train_config.val_data_path,
            batch_size=train_config.val_batch_size,
            input_size=train_config.input[:2],
            classes_no=train_config.number_of_class,
            **gen_params)

        validation_data = val_g.next()

        # Val-test generators
        test_val_generators = [test_g]
        for val_id, val_data_path in enumerate(sorted(train_config.val_data_path)):
            val = train_config.testval_generator(
                data_file=val_data_path,
                batch_size=train_config.val_batch_size,
                input_size=train_config.input[:2],
                classes_no=train_config.number_of_class,
                **gen_params)

            try:
                name_parts = val_data_path.split("/")
                val_index = name_parts.index("val")
                val.name = name_parts[val_index - 1]
            except Exception:
                val.name = "val{}".format(val_id)

            test_val_generators.append(val)

        return g, validation_data, test_val_generators

    else:
        return g, None, [test_g]


def get_model(train_config):
    from vision.keras.models import models
    from keras import utils

    weights = getattr(train_config, "weights", None)
    model = models.get_model(
        name=train_config.model_name,
        class_number=train_config.number_of_class,
        activation=train_config.last_activation,
        input_shape=train_config.input,
        lock_first_layers=train_config.lock_first_layers,
        weights=weights)

    if getattr(train_config, "load_checkpoint", False):
        try:
            checkpoint_glob = train_config.load_checkpoint

            if checkpoint_glob == "[AUTO]":
                checkpoint_glob = train_config.checkpoint_path

            if not checkpoint_glob.endswith(".hdf5"):
                checkpoint_glob += "/**/model*.hdf5"

            checkpoints = glob(checkpoint_glob, recursive=True)
            checkpoints.sort(key=os.path.getmtime)
            checkpoint = checkpoints[-1]

            print("INFO Loading weights from:", checkpoint)
            model.load_weights(checkpoint)
        except Exception as e:
            print("ERROR Cannot load model weights. Error: {}".format(e))

    if train_config.gpus > 1:
        serial_model = model
        model = utils.multi_gpu_model(model, gpus=train_config.gpus)
        # need to set callback model to save weights properly
        model.callback_model = serial_model

    return model


def get_optimizer(train_config):
    from keras import optimizers
    optimizers = {
        'sgd': optimizers.SGD,
        'rmsprop': optimizers.RMSprop,
        'adagrad': optimizers.Adagrad,
        'adadelta': optimizers.Adadelta,
        'adam': optimizers.Adam,
        'adamax': optimizers.Adamax,
        'nadam': optimizers.Nadam,
        'tfoptimizer': optimizers.TFOptimizer,
    }
    return optimizers[train_config.optimizer](lr=train_config.lr)


def f1score_spec_hard(gt, prediction):
    f1score = f1score_spec(prediction=prediction, gt=gt, per_class=True)
    hard_indexes = [3, 4, 8, 9, 13, 14]
    return np.mean(f1score[hard_indexes])


def f1score_spec_optimized(gt, prediction):
    thresholds = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.90, 0.95, 0.99, 0.999])
    fscores = []
    for t in thresholds:
        p = prediction.copy()
        for i in range(p.shape[0]):
            p[i, :-1][p[i, :-1] < t] = 0
            # If none of the face classes reached threshold; assign score=1 to the UNKNOWN class
            if np.max(p[i, 1:-1]) < t:
                p[i, 0] = 1.0

        fscores.append(f1score_spec(prediction=p, gt=gt))
    best = int(np.argmax(fscores))
    return fscores[best], thresholds[best]


def f1score_spec_optimized_val(gt, prediction):
    return f1score_spec_optimized(prediction=prediction, gt=gt)[0]


def f1score_spec_optimized_t(gt, prediction):
    return f1score_spec_optimized(prediction=prediction, gt=gt)[1]


def f1score_spec(*a, **kw):
    return multilabel.f1score_spec(*a, **kw, per_class=False, nan_as_one=True)


def f1score_spec_perclass(*a, **kw):
    return multilabel.f1score_spec(*a, **kw, per_class=True, nan_as_one=True)


def get_callbacks(train_config, test_g, dir_path, datetime_str):
    from keras import callbacks
    from vision.keras.train import callbacks as custom_callbacks

    csv_logger = callbacks.CSVLogger(os.path.join(dir_path, "{}.csv".format(train_config.out_name)))

    checkpoint_callback = callbacks.ModelCheckpoint(
        os.path.join(dir_path, "model-{epoch:02d}-{val_loss:.2f}.hdf5"),
        monitor=train_config.monitoring_measure,
        verbose=train_config.verbose_level,
        period=train_config.checkpoint_interval,
        save_best_only=False,
        save_weights_only=True)

    early_stopping = callbacks.EarlyStopping(
        monitor=train_config.monitoring_measure,
        min_delta=train_config.early_stopping_min_delta,
        patience=train_config.early_stopping_patience,
        verbose=train_config.verbose_level)

    monitor = custom_callbacks.MonitorCallback(
        name="{} {}".format(train_config.out_name, datetime_str))

    tb_dir = os.path.join(dir_path, "tb")

    tensorboard = callbacks.TensorBoard(
        log_dir=tb_dir,
        batch_size=train_config.train_batch_size)

    validate_test = custom_callbacks.TestEvaluator(
        test_g,
        metrics=[
            multilabel.accuracy,
            multilabel.sensitivity,
            multilabel.specificity,
            multilabel.f1score,
            f1score_spec,
        ],
        labels=get_class_names(train_config),
        cm_tb_callback_cm=tensorboard,
        cm_save_dir=os.path.join(dir_path, "cm")
    )

    lr_schedule = callbacks.LearningRateScheduler(lambda epoch, lr: lr / (1. + train_config.decay))
    lr_logger = custom_callbacks.LRLogger()

    callbacks = [
        validate_test, lr_logger, csv_logger, checkpoint_callback,
        early_stopping, tensorboard, monitor, lr_schedule
    ]

    return callbacks


def get_class_names(train_config):
    with open(train_config.mapping_path, "r") as f:
        mapping = json.load(f)
    reverted_mapping = {v: k for k, v in mapping.items()}
    names = [reverted_mapping[i] for i in range(train_config.number_of_class)]
    return names


if __name__ == "__main__":
    tensorflow_use_gpus(1)
    from shelves.models.classification.config import config

    train_model(config.meals_multilabel)
