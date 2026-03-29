from vision.config.main import *


@apply_config
class config(config):
    class aug(Config):
        aug_data_dir = "/tytan/raid/neuca/data/orig/_augmentables"
        fonts_dir = f"{aug_data_dir}/fonts"
        contours_dir = f"{aug_data_dir}/contours"
        normal_latin_fonts_dir = f"{fonts_dir}/normal-latin/"
        dict_path = f"{aug_data_dir}/dicts/odm.txt"
        distribution_path = f"{aug_data_dir}/distribution.json"

    class params(aug):
        # number of threads
        workers = 1
        augmented_per_real_number = 10
        # number of OCR images to generate
        ocr_gen_iterations = 20000
        # number of dummy images to generate
        dummy_gen_iterations = 20000
        # number of front images to generate
        front_gen_iterations = 20000

        train_ratio = .9
        val_ratio = .1

        random_bg_flip = .8
        random_crop_flip = .5

        # random or related positions of dates and serial numbers
        random_positions = 0.1
        related_positions = 1 - random_positions

        # vertical or horizontal orientation of date and serial number crops
        #   (when their positions are related)
        vertical_orientation = 0.85
        horizontal_orientation = 1 - vertical_orientation

        # breaks between crops when positions are vertically oriented
        max_vertical_break = 10
        min_vertical_break = 4

        # breaks between crops when positions are horizontally oriented
        max_horizontal_break = 50
        min_horizontal_break = 25

        # probability of alignment during the vertical orientation
        align_left = .6
        align_right = .3
        align_random = 1 - align_left - align_right

        max_serial_number_length = 20
        bright_text_threshold = 100
        inserted_text_scale = .85

        # max number of iterations to find two random positions
        get_position_limiter = 10

        # max number of iterations to find the widest random crop in given area
        max_widest_crop_iterations = 100

        # max number of attempts to insert synthetic data into the real one
        max_number_of_attempts = 10

        # max number of iterations to find random rect in given area
        iterations_limiter = 1000
