from __future__ import print_function, unicode_literals, absolute_import

from multiprocessing import Pool
from threading import Lock

from vision.aocr.config import load_config_from_checkpoint
from vision.aocr.helpers import *
from vision.monitor import monitor


class AOCR_Base(object):
    def __init__(self, phase, config):
        import tensorflow as tf
        from .aocr.model.model import Model

        self.config = config

        if self.config.custom_confidence:
            self.config.return_raw = True

        self.session = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
        self.model = Model(phase, session=self.session, **self.config.asdict())
        self.lock = Lock()

    def __del__(self):
        self.session.close()

    def predict(self, images):
        with self.lock:
            for text, confidence, raw in self.model.predict_auto(images):
                if self.config.custom_confidence:
                    confidence = self.calc_confidence(raw)
                yield text, confidence

    def test(self):
        with self.lock:
            if not dataset_exists(self.config.dataset_path):
                generate_datasets(self.config)
            self.model.test(data_path=os.path.join(self.config.dataset_path, "test"), verbose=True)

    def calc_confidence(self, raw):
        if raw is None:
            raise Exception("NN must return raw values to calculate confidence!")

        n = 0
        for n in range(len(raw)):
            line = raw[n]
            if line.argmax() == 2:
                break

        if n == 0:
            return 0

        word = raw[:n]
        confidence = word.max(axis=1).mean()
        print("DEBUG confidence", confidence)
        confidence = sigmoid(confidence, *self.config.custom_confidence)
        return max(0, min(1, confidence))


class AOCR(AOCR_Base):
    checkpoint = "/kolos/m2/ocr/aocr/training/all-chars-aug12/"

    def __init__(self, checkpoint=None, **override_config):
        if checkpoint:
            self.checkpoint = checkpoint

        if not self.checkpoint:
            raise Exception("No aocr checkpoint provided")

        config = load_config_from_checkpoint(self.checkpoint)
        
        for name, value in six.iteritems(override_config):
            setattr(config, name, value)

        super(AOCR, self).__init__("test", config)


class AOCR_Train(AOCR_Base):
    def __init__(self, config=None, checkpoint=None, **override_config):
        if (not config and not checkpoint) or (config and checkpoint):
            raise ValueError()

        if config:
            config = load_config(config).instance()

        if checkpoint:
            config = load_config_from_checkpoint(checkpoint)

        for name, value in six.iteritems(override_config):
            setattr(config, name, value)

        super(AOCR_Train, self).__init__("train", config)
        monitor.GROUP = "AOCR Train: " + self.config.name

    def append_to_datasets(self):
        monitor.starting(tag="Database")
        append_to_datasets(self.config)
        monitor.finished(tag="Database")

    def generate_datasets(self):
        monitor.starting(tag="Database")
        generate_datasets(self.config)
        monitor.finished(tag="Database")

    def train(self):
        logging.info("Training " + self.config.name)

        self.config.save()
        self.config.visualize = False
        self.config.show_incorrect = False
        self.config.show_correct = False
        self.config.show_raw = False

        if self.config.append_to_existing:
            self.append_to_datasets()
        elif not dataset_exists(self.config.dataset_path):
            self.generate_datasets()
        else:
            logging.info("Using existing dataset: " + self.config.dataset_path)

        logging.info("Training started")
        monitor.starting(tag="Step")

        self.model.train(
            data_path=os.path.join(self.config.dataset_path, "train"),
            data_path_val=os.path.join(self.config.dataset_path, "val"),
            num_epoch=self.config.num_epoch)

        logging.info("Training finished.")


class AOCR_Search(object):
    def __init__(self, config_name):
        self.config_name = config_name
        self.config = load_config(config_name)

    def dataset(self):
        if dataset_exists(self.config.dataset_path):
            logging.info("Using existing dataset: " + self.config.dataset_path)
            return

        pool = Pool(1)
        pool.apply(generate_datasets, [self.config_name])
        pool.close()
        pool.join()

    def search(self):
        pool = None
        try:
            self.dataset()

            pool = Pool(self.config.processes)
            logging.debug("Pool size: {}".format(pool._processes))

            logging.info("Starting search...")
            for ret in pool.imap_unordered(train, [self.config_name for _ in range(1000)]):
                if ret is KeyboardInterrupt:
                    raise KeyboardInterrupt
            logging.info("Search finished")

        except KeyboardInterrupt:
            logging.error("Keyboard interrupt")
            if pool is not None:
                pool.close()
                pool.terminate()
                pool.join()
            exit(1)
