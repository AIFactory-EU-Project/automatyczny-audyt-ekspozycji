from vision.tensorflow.gpus import tensorflow_use_gpus
from vision.aocr.api import AOCR

if __name__ == '__main__':
    tensorflow_use_gpus(1)
    checkpoint = r"/tytan/raid/neuca/models/aocr/v1/models/"
    ocr = AOCR(checkpoint, batch_size=2)
    ocr.test()
