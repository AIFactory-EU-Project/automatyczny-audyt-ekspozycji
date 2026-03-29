import os
import random
import cv2
import numpy as np
import aug

from enum import Enum
from PIL import Image, ImageFont, ImageDraw

from ocr.aug.word_generators.values_generator import TextValueGenerator
from ocr.aug.distribution import DistributionConfig
from ocr.aug.config import config
from vision.aug.transformations.transformation import Transformation


class Type(Enum):
    SERIAL_NUMBER = 0
    DATE = 1


class TextGenerator:
    FONT_SIZE = (80, 100)
    FONTS_DIR = config.aug.fonts_dir
    SPACE_OUT_PROBABILITY = .75
    BLACK_TEXT_COLOR_RANGE = (0, 80)
    WHITE_TEXT_COLOR_RANGE = (180, 254)

    distribution = DistributionConfig()

    def __init__(self, transformation_ops=None):
        self.config_class = None
        self.config = None
        self.fonts_path = self.FONTS_DIR
        self.font_type = ""
        self.font_name = ""
        self.mode = None
        self.text_color = None
        self.bg_color = None
        self.transformation_ops = transformation_ops
        self.text_generator = TextValueGenerator()

    def load_font(self, path=None, font_type=None, font_size=None, font_dir=None):
        """ Load random font file from the given directory """
        if path is None:
            path = self.fonts_path

        self.font_type = font_type
        if self.font_type is None:
            self.font_type = self.distribution.get_font_type()

        if font_size is None:
            font_size = random.randint(*self.FONT_SIZE)

        if font_dir is None:
            font_dir = self.font_type

        path = os.path.join(path, font_dir)
        file_names = os.listdir(path)
        assert len(file_names) > 0
        index = random.randint(0, len(file_names) - 1)
        path = os.path.join(path, file_names[index])

        font = ImageFont.truetype(path, font_size)
        self.font_name = file_names[index]

        return font

    @staticmethod
    def join_text_and_background(text_img, bg_img):
        txt = Image.fromarray(text_img)
        background = Image.fromarray(bg_img).convert("RGBA")
        out = Image.alpha_composite(background, txt)
        image = np.array(out)
        return image

    def get_font_type(self):
        return self.font_type

    def get_text_color(self):
        return self.text_color

    def get_font_name(self):
        return self.font_name

    def get_background_img(self, in_image):
        height, width = in_image.shape[:2]
        image = np.zeros((height, width, 3), dtype=np.uint8)
        image[:] = self.bg_color

        return image

    @staticmethod
    def generate_img(font, text_tmp, color=None):
        assert color is not None

        font_size = font.getsize(text_tmp)
        txt = Image.new("RGBA", font_size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), text_tmp, font=font, fill=color)
        txt_cv = np.array(txt, dtype=np.uint8)

        return txt_cv

    def get_text_img(self, font, text, bg=None):
        text_tmp = text
        if random.random() < self.SPACE_OUT_PROBABILITY and self.font_type != "dotted":
            text_tmp = ''
            spaces = random.randint(1, 2) * ' '
            for i in range(len(text) - 1):
                text_tmp += text[i] + spaces
            text_tmp += text[-1]

        if bg is not None:
            self.set_colors(bg)
        else:
            # if background is unknown then the text color is black
            self.set_dark_text_color_config()

        txt_cv = self.generate_img(font, text_tmp, self.text_color)
        return txt_cv

    def get_processed_text_img(self, text):
        font = self.load_font()

        text_img = self.get_text_img(font, text)
        text_img = Transformation.fit_borders(text_img)
        # apply text transformations
        if self.transformation_ops:
            ops_pipeline = self.transformation_ops[self.font_type].text_ops
            if ops_pipeline:
                text_img = ops_pipeline.apply(aug.Sample(image=text_img.copy())).image
        return text_img

    def generate(self, text):
        text_img = self.get_processed_text_img(text)
        background_img = self.get_background_img(text_img)
        background_img = self.config_class.apply_background_transformations(background_img)

        image = self.join_text_and_background(text_img, background_img)
        image = self.config_class.apply_composite_transformations(image)

        return image

    def get_date_value(self):
        self.mode = Type.DATE
        return self.text_generator.get_date_value()

    def get_serial_number_value(self, length=None):
        self.mode = Type.SERIAL_NUMBER
        return self.text_generator.get_serial_number_value(length)

    def get_dummy_text(self):
        return self.text_generator.get_dummy_text()

    def get_single_date_image(self):
        value = self.get_date_value()
        return value, self.generate(value)

    def get_single_serial_number_image(self):
        value = self.get_serial_number_value()
        return value, self.generate(value)

    def get_fixed_size_random_raw_crop(self, shape):
        if random.getrandbits(1):
            self.text = self.get_serial_number_value()
        else:
            self.text = self.get_date_value()

        font = self.load_font()
        text_img = self.get_text_img(font, self.text)
        text_img = Transformation.fit_borders(text_img)
        text_img = cv2.resize(text_img, shape, interpolation=cv2.INTER_CUBIC)

        return text_img

    def random_colors(self, bg_hsv, text_color_range):
        self.text_color = tuple(3*[random.randint(*text_color_range)])
        self.bg_color = cv2.cvtColor(cv2.cvtColor(bg_hsv, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2RGB)

    def set_bright_text_color_config(self):
        bg_hsv = np.array([[[random.randint(0, 360), random.randint(0, 200), random.randint(30, 120)]]], dtype=np.uint8)
        text_color_range = self.WHITE_TEXT_COLOR_RANGE
        self.random_colors(bg_hsv, text_color_range)

    def set_dark_text_color_config(self):
        bg_hsv = np.array([[[random.randint(0, 360), random.randint(0, 50), random.randint(100, 255)]]], dtype=np.uint8)
        text_color_range = self.BLACK_TEXT_COLOR_RANGE
        self.random_colors(bg_hsv, text_color_range)

    def set_colors(self, background):
        """ Set random colors of letters and the background """
        bg = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
        average = np.average(bg)

        if average < config.params.bright_text_threshold and not self.is_dotted():
            self.set_bright_text_color_config()
        else:
            self.set_dark_text_color_config()

    def is_dotted(self):
        return "dotted" in self.font_name
