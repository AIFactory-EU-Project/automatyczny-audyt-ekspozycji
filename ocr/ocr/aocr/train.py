from ocr.aocr.config import config

from vision.aocr.api import AOCR_Train
from vision.tensorflow.gpus import tensorflow_use_gpus

if __name__ == '__main__':
    tensorflow_use_gpus(1)

    config = config.boxes.ocr_base
    ocr = AOCR_Train(config)
    ocr.train()

    # config = config.boxes.all_chars_updown
    # config.override["data_train"] = config.data_train
    # config.override["data_val"] = config.data_val
    # config.override["data_test"] = config.data_test
    #
    # ckpt = "/tytan/raid/neuca/models/aocr/all-chars-aug13-updown/"
    # ocr = AOCR_Train(checkpoint=ckpt, **config.override)
    # ocr.train()

