#!/usr/bin/env python2

from __future__ import absolute_import, unicode_literals, print_function

import logging
import os
import six
from multiprocessing import Pool
from time import sleep

from vision.helpers.file_helpers import makedirs
from .config import load_config

# todo need refactor


def train(args):
    ident, config = args
    try:
        if ident < 8:
            logging.debug("Sleeping {} seconds".format(ident*10))
            sleep(ident*10)

        from .train import train

        config = load_config(config)
        config = config.instance()

        logging.info("Training hyperparameters:")
        for name, value in six.iteritems(config.asdict()):
            # forms char_map contains non-ascii characters
            if name == "char_map":
                value = value.encode('utf-8')
            logging.info("\t{name}: {value}".format(**locals()))

        if os.path.isdir(config.model_dir):
            logging.warn("Run path exists: " + config.model_dir)

        makedirs(config.model_dir)
        config.save()

        train(config)
    except Exception as e:
        logging.error("Error during training. Breaking. " + str(e))
        raise
    except KeyboardInterrupt:
        logging.error("Trainning thread interrupted")
        return KeyboardInterrupt


def dataset(config):
    config = load_config(config)

    if os.path.isdir(config.dataset_path):
        logging.info("Using existing dataset: " + config.dataset_path)
        return

    if config.type == "forms":
        from .forms_aocr.generate_datasets import generate_forms_datasets
        generate_forms_datasets(config.src_path, config.dataset_path, config.shuffle)
    else:
        from dataset import generate_datasets_auto
        generate_datasets_auto(config)


def search(config_name):
    config = load_config(config_name)

    pool = Pool(config.processes)
    logging.debug("Pool size: {}".format(pool._processes))

    try:
        logging.info("Generating datasets...")

        pool.apply(dataset, [config_name])

        logging.info("Starting search...")
        for ret in pool.imap_unordered(train, [(i,config_name) for i in xrange(1000)]):
            if ret is KeyboardInterrupt:
                raise KeyboardInterrupt

        logging.info("Search finished")
    except KeyboardInterrupt:
        logging.error("Keyboard interrupt")
        pool.close()
        pool.terminate()
        pool.join()
        exit(1)


if __name__ == '__main__':
    search("config_boxes.config.boxes.search")

