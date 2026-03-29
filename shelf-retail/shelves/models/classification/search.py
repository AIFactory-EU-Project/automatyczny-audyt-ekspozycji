import os
from datetime import datetime
from hopt import search

from shelves.models.classification import train as meals_train
from vision.tensorflow.gpus import tensorflow_use_gpus
from vision.metrics.numpy import multilabel


def train_model(train_config):
    from vision.keras.train import train as train_utils

    # data
    g, validation_data, test_g = meals_train.get_data_generators(train_config)
    validation_steps = train_config.validation_steps if train_config.use_validation else None

    # model
    model = meals_train.get_model(train_config)
    metrics_names = getattr(train_config, "metrics", [])
    metrics = train_utils.get_metrics(metrics_names)
    loss = train_utils.get_loss(train_config.loss_func)
    optimizer = meals_train.get_optimizer(train_config)
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    # callbacks
    callbacks = get_callbacks(train_config, test_g)

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


def get_callbacks(train_config, test_g):
    from keras import callbacks
    from hopt.keras import HoptCallback
    from vision.keras.train import callbacks as custom_callbacks

    hopt_callback = HoptCallback(
        metric_monitor='test_f1score_spec',
        metric_lower_better=False,
        model_prefix='test_f1score_spec-{test_f1score_spec:05.3f}_{epoch:02d}',
        keep_models=1)

    validate_test = custom_callbacks.TestEvaluator(
        [test_g[0]],
        metrics=[
            multilabel.accuracy,
            multilabel.sensitivity,
            multilabel.specificity,
            multilabel.f1score,
            meals_train.f1score_spec,
            meals_train.f1score_spec_optimized_val,
            meals_train.f1score_spec_optimized_t
        ],
        labels=meals_train.get_class_names(train_config))

    lr_schedule = callbacks.LearningRateScheduler(lambda epoch, lr: lr / (1. + train_config.decay))

    callbacks = [validate_test, lr_schedule, hopt_callback]

    return callbacks


if __name__ == "__main__":
    tensorflow_use_gpus(1)
    from shelves.models.classification.config import config

    datetime_str = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cfg = config.meals_multilabel_hyperparam_search

    search(
        train_function=train_model,
        hyperparams=cfg,
        out_dir=os.path.join(cfg.out_dir, datetime_str),
        iterations=cfg.search_iter,
    )
