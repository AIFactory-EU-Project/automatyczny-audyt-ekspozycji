import glob
import time

import cv2
import six
from vision.caffe.general.classify import MultiSingleCategoryClassifier, SingleClassifier
from vision.config.auto import *


@auto_config
class config(config):

    class sleeve_sqn1(Config):
        transforms = None

        class default(Config):
            caffe_path = '{caffe.default_home}'
            gpu_id = '{caffe.default_gpu}'

        class model(default):
            home = '/tytan/raid/fashion/categorization/models/etfa2017/sleeve-type/sqn-single'
            wrapper = 'SqueezeNet'
            batchsize = 607

    class sleeve_sqn5(Config):
        transforms = None

        class default(Config):
            caffe_path = '{caffe.default_home}'
            gpu_id = '{caffe.default_gpu}'

        class model(default):
            home = '/tytan/raid/fashion/categorization/models/etfa2017/sleeve-type/sqn-ensemble5'
            wrapper = 'SqueezeNet'
            batchsize = 115

    class sleeve_res1(Config):
        transforms = None

        class default(Config):
            caffe_path = '{caffe.default_home}'
            gpu_id = '{caffe.default_gpu}'

        class model(default):
            home = '/tytan/raid/fashion/categorization/models/etfa2017/sleeve-type/resnet50-single'
            wrapper = 'Resnet'
            batchsize = 60

    class sleeve_res5(Config):
        transforms = None

        class default(Config):
            caffe_path = '{caffe.default_home}'
            gpu_id = '{caffe.default_gpu}'

        class model(default):
            home = '/tytan/raid/fashion/categorization/models/etfa2017/sleeve-type/resnet50-ensemble5'
            wrapper = 'Resnet'
            batchsize = 10


classifiers = {
    "sqn1": config.sleeve_sqn1,
    "sqn5": config.sleeve_sqn5,
    "res1": config.sleeve_res1,
    "res5": config.sleeve_res5
}


if __name__ == "__main__":
    n = 10000
    paths = glob.glob("/tytan/raid/fashion/data/nokaut/Dresses/*/*.jpg")[:n]
    imgs = [cv2.imread(p) for p in paths]
    n = len(paths)
    print("ONE PICTURE MODE")
    for name, conf in six.iteritems(classifiers):
        c = MultiSingleCategoryClassifier([conf])
        t1 = time.time()
        for i in range(n):
            c.get_result(imgs[i])

        t2 = time.time()

        print("{} - {}s".format(name, (t2 - t1) / n))
        del c

    print("BATCH MODE")
    for name, conf in six.iteritems(classifiers):
        c = SingleClassifier(conf)
        t1 = time.time()
        batch = []
        batch_size = conf.model.batchsize
        for img in imgs:
            batch.append(img)
            if len(batch) == batch_size:
                c.detect(batch)
                batch = []
        t2 = time.time()

        print("{} - {} FPS".format(name, n / (t2 - t1)))
        del c


