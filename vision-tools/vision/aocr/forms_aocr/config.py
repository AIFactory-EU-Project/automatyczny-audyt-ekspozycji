# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals


from vision.aocr.config import *

from .data import form_samples


@auto_config
class config(config):
    class forms(config.aocr):
        class base(config.aocr.base):
            home_dir = "/tytan/raid/form-reader/models/"
            src_path = "/tytan/raid/form-reader/datasets/ocr_dataset/.../labels.txt"
            training_dir = "{}/training".format(home_dir)
            name = "v2"
            shuffle = True
            max_width = 512
            max_height = 32
            max_prediction = 128
            char_map = r""" ,?"'.`-/\@$^*_!#%+&={{}}:;<>|0123456789AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻaąbcćdeęfghijklłmnńoópqrsśtuvwxyzźżüëöäű"""
            uppercase = False
            batch_size = 64
            online_augmentation = False

            @classmethod
            def data_train(cls):
                return form_samples(path=cls.src_path.replace("...", "train"), paths_only=True)

            @classmethod
            def data_test(cls):
                return form_samples(path=cls.src_path.replace("...", "test"), paths_only=True)

            @classmethod
            def data_val(cls):
                return form_samples(path=cls.src_path.replace("...", "val"), paths_only=True)

        class search(base):
            """Base class for random hyperparameter search"""
            type = "forms"
            name = "search-v2"
            run = "unknown-run"

            dataset_path = "{training_dir}/{name}/data"
            model_dir = "{training_dir}/{name}/{{run}}"

            num_epoch = 60
            processes = 1

            target_embedding_size = IntParam(5, 50)  # default: 10
            attn_num_hidden = IntParam(16, 256)  # default: 128
            attn_num_layers = IntParam(2, 2)  # default: 2
            max_gradient_norm = FloatParam(1, 10)  # default: 5.0
            dropout = FloatParam(0, 0.8)  # default: 0.5

        class test(base):
            name = "v2"
            steps_per_checkpoint = 100
            steps_per_test = 100
            visualize = False
            show_incorrect = False

        class jachootest(base):
            name = "jachootest4"
            batch_size = 3
            steps_per_test = 10
