import logging
import math
import os
import random
import six

from vision.aocr.config import load_config
from vision.helpers.file_helpers import makedirs


def sigmoid(x, min, max):
    # min -> -6
    # max -> 6
    c = (max+min)*0.5
    l = max-min
    x = 8.*(x-c)/l
    return 1 / (1 + math.exp(-x))


def dataset_exists(path):
    try:
        return os.path.getsize(os.path.join(path, "train")) and os.path.getsize(os.path.join(path, "test"))
    except Exception:
        return False


def generate_datasets(config):
    config = load_config(config)
    logging.info("Generating datasets: {}".format(config.dataset_path))

    if dataset_exists(config.dataset_path):
        logging.warn("Overriding dataset!")

    makedirs(config.dataset_path)
    logging.info("Reading train/test filelists")

    train = list(config.data_train())
    val = list(config.data_val())
    test = list(config.data_test())

    logging.info("Shuffling data...")
    random.shuffle(train)
    random.shuffle(val)
    random.shuffle(test)

    from .aocr.util.dataset import generate_iter

    logging.info("Generating training data files ({} records)".format(len(train)))
    generate_iter(train, os.path.join(config.dataset_path, "train"), force_uppercase=config.uppercase, substitutions=config.char_subst)

    logging.info("Generating validating data files ({} records)".format(len(val)))
    generate_iter(val, os.path.join(config.dataset_path, "val"), force_uppercase=config.uppercase, substitutions=config.char_subst)

    logging.info("Generating testing data files ({} records)".format(len(val)))
    generate_iter(val, os.path.join(config.dataset_path, "test"), force_uppercase=config.uppercase, substitutions=config.char_subst)

    logging.info("Datasets generated.")


def append_to_datasets(config):
    config = load_config(config)
    logging.info("Appending to datasets: {}".format(config.dataset_path))

    train = list(config.data_train())
    val = list(config.data_val())
    test = list(config.data_test())

    logging.info("Shuffling data...")
    random.shuffle(train)
    random.shuffle(val)
    random.shuffle(test)

    import tensorflow as tf
    from .aocr.util.dataset import generate_iter
    from vision.aocr.aocr.util.dataset import prepare_tf_example

    for subset, subset_name in zip([train, val, test], ["train", "val", "test"]):
        record_pth = os.path.join(config.dataset_path, subset_name)
        if os.path.exists(record_pth):
            with tf.python_io.TFRecordWriter(os.path.join(config.dataset_path, "tmp")) as writer:
                with tf.Graph().as_default(), tf.Session():
                    ds = tf.data.TFRecordDataset([record_pth])
                    rec = ds.make_one_shot_iterator().get_next()
                    while True:
                        try:
                            writer.write(rec.eval())
                        except tf.errors.OutOfRangeError:
                            break
                for img_pth, label in subset:
                    if img_pth is None or label is None:
                        print("None label or img")
                        continue
                    example = prepare_tf_example(img_pth, label, force_uppercase=config.uppercase, substitutions=config.char_subst, save_filename=False)
                    writer.write(example)

            os.remove(record_pth)
            os.rename(os.path.join(config.dataset_path, "tmp"), record_pth)
        else:
            generate_iter(subset, os.path.join(config.dataset_path, subset_name), force_uppercase=config.uppercase, substitutions=config.char_subst)

    logging.info("Datasets generated")


def train(config):
    try:
        config = load_config(config).instance()
        logging.info("Training hyperparameters:")

        for name, value in six.iteritems(config.asdict()):
            logging.info(u"\t{name}: {value}".format(**locals()))

        if os.path.isdir(config.model_dir):
            logging.warn("Run path exists: " + config.model_dir)

        makedirs(config.model_dir)
        config.save()

        from vision.aocr.api import AOCR_Train
        aocr = AOCR_Train(config)
        aocr.train()

    except Exception as e:
        logging.error("Error during training. Breaking. " + str(e))
        raise

    except KeyboardInterrupt:
        logging.error("Trainning thread interrupted")
        return KeyboardInterrupt

