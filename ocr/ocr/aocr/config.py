import random

from vision.aocr.config import *


@apply_config
class config(config):
    class boxes(config.aocr):
        class ocr_base(config.aocr.base):
            home_dir = "/tytan/raid/neuca"  # base dir
            name = "testing"  # training versioning
            data_dir = f"{home_dir}/data/aocr/v1"  # dir for source data
            training_dir = f"{home_dir}/models/aocr/{name}"  # dir where training will take place
            output_dir = f"{training_dir}/aocr-output"  # temporary output dir
            dataset_path = f"{training_dir}/data"  # dir where TFRecords will be created
            model_dir = f"{training_dir}/models"  # dir where models and checkpoints will be saved
            checkpoint = 0

            aug_dirs = ["/tytan/raid/neuca/data/aocr/aug13"]
                        # "/tytan/raid/neuca/data/aocr/aug15"]  # already augmented data stored on the disk
            shuffle = True
            online_augmentation = False

            max_width = 512
            max_height = 32
            max_prediction = 20
            uppercase = True
            text = False
            char_map = '.-/\\0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            char_subst = {" ": ""}

            return_raw = False
            custom_confidence = None
            batch_size = 64
            num_epoch = 100
            steps_per_checkpoint = 500
            steps_per_test = 500

            visualize = False
            show_correct = False
            show_incorrect = False
            show_raw = False

            # append data to existing tfrecords
            append_to_existing = False

            @staticmethod
            def get_sample(aug_dir, orig_dir, phase):
                with open(os.path.join(orig_dir, phase, "annotations.json"), "r") as f:
                    orig_json_data = json.load(f)
                orig_data = [(k, v) for k, v in orig_json_data.items()]

                with open(os.path.join(aug_dir, phase, "annotations.json"), "r") as f:
                    aug_json_data = json.load(f)

                for aug_pth, aug_value in aug_json_data.items():
                    yield aug_pth, aug_value
                    # balance set (2 times more real data than augmented data)
                    orig_pth, orig_value = random.choice(orig_data)
                    yield orig_pth, orig_value
                    orig_pth, orig_value = random.choice(orig_data)
                    yield orig_pth, orig_value

            @classmethod
            def data_train(cls, validation=False):
                # data used for training
                # data is being saved in tfrecords file and then retrieved for training - need to balance set first
                phase = "train" if not validation else "val"
                train = []
                for aug_dir in cls.aug_dirs:
                    train += cls.get_sample(aug_dir, cls.data_dir, phase)

                return train

            @classmethod
            def data_val(cls):
                return cls.data_train(validation=True)

            @classmethod
            def data_test(cls):
                # test only on the real data
                test = []
                test_pth = os.path.join(cls.data_dir, "test", "annotations.json")
                if not os.path.exists(test_pth):
                    return test

                with open(test_pth, "r") as f:
                    json_data = json.load(f)

                for path, value in json_data.items():
                    test += (path, value)
                return test

        class all_chars(ocr_base):
            augmentation = ["aug13", "aug14"]
            name = "all-chars-aug13"
            max_width = 512
            max_prediction = 50
            batch_size = 128
            uppercase = False
            text = True
            char_map = u' *0123456789ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz'
            char_subst = {
                ' ': ' ',
                '.': '*',
                ',': '*',
                ';': '*',
                ':': '*',
                '-': '*',
                '_': '*',
                '/': '*',
                '\\': '*',
                '+': '*',
                '%': '*',
                "'": '*',
                '"': '*',
                '?': '*',
                u'°': '*',
                '(': '*',
                ')': '*',
                '[': '*',
                ']': '*',
                '{': '*',
                '}': '*',
                '<': '*',
                '>': '*',

                'O': '0',
                'i': '1',
                'l': '1',
                'o': '0',

                u'ą': 'a',
                u'ć': 'c',
                u'ę': 'e',
                u'ł': '1',
                u'ń': 'n',
                u'ó': '0',
                u'ś': 's',
                u'ź': 'z',
                u'ż': 'z',

                u'Ą': 'A',
                u'Ć': 'C',
                u'Ę': 'E',
                u'Ł': 'L',
                u'Ń': 'N',
                u'Ó': '0',
                u'Ś': 'S',
                u'Ź': 'Z',
                u'Ż': 'Z',

                u'é': 'e',  # nie powinno byc w danych!
            }

        class all_chars_updown(all_chars):
            name = "all-chars-aug13-updown"

            aug_dirs = ["/tytan/raid/neuca/data/aocr/augs/gen/v1"]
            online_augmentation = True
            append_to_existing = True

            override = {
                "name": name,
                "aug_dirs": aug_dirs,
                "append_to_existing": append_to_existing
            }

        class search(all_chars):
            """Base class for random hyperparameter search"""
            name = "search-aug10-testtesttest3"
            run = "unknown-run"

            dataset_path = "{training_dir}/{name}/data"
            model_dir = "{training_dir}/{name}/{{run}}"

            num_epoch = 100
            processes = 1

            target_embedding_size = IntParam(5, 50)  # default: 10
            attn_num_hidden = IntParam(16, 256)  # default: 128
            attn_num_layers = IntParam(2, 2)  # default: 2
            max_gradient_norm = FloatParam(1, 10)  # default: 5.0
            dropout = FloatParam(0, 0.8)  # default: 0.5
