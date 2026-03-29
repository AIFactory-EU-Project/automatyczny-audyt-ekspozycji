import os
import sys
from datetime import datetime
from pprint import pprint

from vision.config.config import all_vars
from vision.tensorflow.gpus import tensorflow_use_gpus


def create_dir_for_training(log_path, datetime_str):
    dir_path = os.path.join(log_path, datetime_str)
    os.makedirs(dir_path)
    return dir_path


def get_metrics(metrics_names):
    from keras import metrics as keras_metrics
    from vision.keras.train import metrics as custom_metrics

    metrics = []
    for metric_name in metrics_names:
        metric = custom_metrics.get(metric_name)
        if not metric:
            metric = keras_metrics.get(metric_name)
        metrics.append(metric)
    return metrics


def get_loss(name):
    from keras import losses as keras_losses
    from vision.keras.train import losses as custom_losses

    loss_func = custom_losses.get(name)
    if not loss_func:
        loss_func = keras_losses.get(name)

    return loss_func


def train_model(train_config):
    tensorflow_use_gpus(train_config.gpus)

    from keras import callbacks
    from keras import utils
    from vision.keras.models import models
    from vision.keras.train import callbacks as custom_callbacks
    from vision.keras.train import generator
    from vision.keras.train import logger

    datetime_str = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dir_path = create_dir_for_training(train_config.logging_path, datetime_str)
    # log to screen and file
    output = logger.Logger(os.path.join(dir_path, "log.log"))
    sys.stdout = output

    # print configuration
    pprint(all_vars(train_config))

    # data generators
    gen_params = getattr(train_config, "generator_params", {})
    g = generator.Generator(batch_generator=train_config.generator, data_file=train_config.data_path, batch_size=train_config.train_batch_size,
                            input_size=train_config.input[:2], **gen_params)
    val_g = generator.Generator(batch_generator=train_config.val_generator, data_file=train_config.val_data_path, batch_size=train_config.val_batch_size,
                                input_size=train_config.input[:2], **gen_params)

    # validation
    validation_data = val_g.next() if train_config.use_validation else None
    validation_steps = train_config.validation_steps if train_config.use_validation else None

    # model
    weights = getattr(train_config, "weights", None)
    model = models.get_model(train_config.model_name, train_config.number_of_class, activation=train_config.last_activation,
                             input_shape=train_config.input, lock_first_layers=train_config.lock_first_layers, weights=weights)
    model.summary()

    if train_config.gpus > 1:
        serial_model = model
        model = utils.multi_gpu_model(model, gpus=train_config.gpus)
        # need to set callback model to save weights properly
        model.callback_model = serial_model

    # metrics
    metrics_names = getattr(train_config, "metrics", [])
    metrics = get_metrics(metrics_names)

    # loss
    loss = get_loss(train_config.loss_func)
    model.compile(optimizer=train_config.optimizer, loss=loss, metrics=metrics)

    # callbacks
    csv_logger = callbacks.CSVLogger(os.path.join(dir_path, "{}.csv".format(train_config.out_name)))
    checkpoint_callback = callbacks.ModelCheckpoint(os.path.join(dir_path, "{}.hdf5".format(train_config.out_name)),
                                                    monitor=train_config.monitoring_measure, verbose=train_config.verbose_level,
                                                    period=train_config.checkpoint_interval, save_best_only=True, save_weights_only=True)
    early_stopping = callbacks.EarlyStopping(monitor=train_config.monitoring_measure, min_delta=train_config.early_stopping_min_delta,
                                             patience=train_config.early_stopping_patience, verbose=train_config.verbose_level)
    monitor = custom_callbacks.MonitorCallback("{} {}".format(train_config.out_name, datetime_str))
    tensorboard = callbacks.TensorBoard(os.path.join(dir_path, "tb"), batch_size=train_config.train_batch_size)

    callbacks = [csv_logger, checkpoint_callback, early_stopping, tensorboard, monitor]

    # training
    model.fit_generator(g.next(), steps_per_epoch=train_config.steps_per_epoch, epochs=train_config.epochs,
                        verbose=train_config.verbose_level, callbacks=callbacks,
                        validation_data=validation_data, validation_steps=validation_steps, shuffle=False)
