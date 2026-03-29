""" Render text images from strings. """
import random
import cv2

from ocr.aug import aug_utils
from ocr.aug.word_generators.generator import TextGenerator
from vision.aug.transformations.transformation import Transformation


class CroppedTextGenerator(TextGenerator):
    def __init__(self, transformation_ops=None):
        TextGenerator.__init__(self, transformation_ops=transformation_ops)
        self.texts = []

    @staticmethod
    def flip_shape(shape):
        if len(shape) == 3:
            return shape[1], shape[0], shape[2]
        elif len(shape) == 2:
            return shape[1], shape[0]
        else:
            assert shape not in [2, 3]

    def get_fixed_size_crop(self, text, size, font=None, flip=True, direction=None):
        if font is None:
            font = self.load_font()

        vertical = False
        if aug_utils.is_vertically_oriented(shape=(size[1], size[0])):
            vertical = True

        if vertical:
            size = self.flip_shape(size)

        self.texts = text
        text_img = self.get_text_img(font, text)
        text_img = Transformation.fit_borders(text_img)
        text_img = cv2.resize(text_img, size, interpolation=cv2.INTER_CUBIC)

        if vertical and flip:
            if direction is None:
                direction = random.choice([1, 3])
                text_img = aug_utils.flip_image(text_img, direction)
            else:
                text_img = aug_utils.flip_image(text_img, direction)

        return text_img, direction

    def get_fixed_size_pair_of_crops(self, text1, shape1, text2, shape2, bright=False, flip=True):
        self.texts = [text1, text2]
        if bright:
            self.set_bright_text_color_config()
        else:
            self.set_dark_text_color_config()

        font = self.load_font()
        text_img1, direction = self.get_fixed_size_crop(text1, shape1, font, flip)
        text_img2, _ = self.get_fixed_size_crop(text2, shape2, font, flip, direction=direction)
        return text_img1, text_img2


if __name__ == "__main__":
    generator = CroppedTextGenerator()
    for _ in range(50):
        if random.getrandbits(1):
            value, img = generator.get_single_date_image()
        else:
            value, img = generator.get_single_serial_number_image()

        cv2.imshow("img", img)
        cv2.waitKey(0)
