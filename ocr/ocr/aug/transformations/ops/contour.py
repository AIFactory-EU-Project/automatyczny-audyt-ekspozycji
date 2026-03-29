import random
import cv2
import numpy as np

from PIL import Image, ImageDraw

from aug import Operation, perform_randomly
from aug.ops.utils import fit_borders
from aug.ops.contours import Direction, get_cut_letter_coords, get_random_offsets, fit_image_to_available_area
from ocr.aug.base_words.loader import TemplateLoader
from ocr.aug.word_generators.cropped_generator import CroppedTextGenerator
from vision.helpers.file_helpers import i_find_all_images


@perform_randomly
class OcrDrawCutCharacters(Operation):
    """ Insert random contours (characters) in a random position. """
    def __init__(self, direction=None, contour_width=(.6, .9)):
        self._direction = direction
        self._contour_width = contour_width
        self._fonts_dir = ""
        self._generator = CroppedTextGenerator()

    def apply_on_image(self, image):
        b_max = int(.45 * image.shape[0])
        if self._direction is None:
            self._direction = Direction(random.randint(0, 3))

        cut_text_font_size = int(random.uniform(.8, 1.2) * image.shape[0])
        image = cv2.copyMakeBorder(image, b_max, b_max, b_max, b_max, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255, 0))
        coords = get_cut_letter_coords(self._direction, b_max, image.shape, self._contour_width)

        mode = "serial" if random.getrandbits(1) else "date"
        if random.getrandbits(1):
            if mode == "serial":
                text = self._generator.get_serial_number_value()
            else:
                text = self._generator.get_date_value()
        else:
            text = TemplateLoader(mode).get_random_expr()

        font = self._generator.load_font(font_type="normal", font_dir="normal-latin", font_size=cut_text_font_size)

        cut_text = Image.new("RGBA", font.getsize(text), (255, 255, 255, 0))
        d = ImageDraw.Draw(cut_text)
        self._generator.set_colors(np.array(cut_text))
        d.text((0, 0), text, font=font, fill=self._generator.get_text_color())
        cut_text = np.array(cut_text)
        cut_text = fit_borders(cut_text)
        cut_text = fit_image_to_available_area(cut_text, self._direction, coords)

        x_offset, y_offset = get_random_offsets(self._direction, coords, cut_text)
        image[y_offset + coords[0][1]:y_offset + coords[0][1] + cut_text.shape[0], x_offset + coords[0][0]:x_offset + coords[0][0] + cut_text.shape[1]] = cut_text
        image = fit_borders(image)
        return image


@perform_randomly
class OcrTemplateContour(Operation):
    """ Load contour from image file and insert in a random position """
    def __init__(self, direction=None, contour_width=(.6, .9), margin=None):
        contour_pth = "/tytan/raid/neuca/data/orig/_augmentables/contours"
        contours = [cv2.cvtColor(cv2.imread(c), cv2.COLOR_RGB2RGBA) for c in i_find_all_images(contour_pth)]
        self._contour = random.choice(contours)
        self._direction = direction
        self._contour_width = contour_width
        self._margin = margin

    def apply_on_image(self, image):
        h = int(random.uniform(.8, 2) * image.shape[0])
        w = int(self._contour.shape[1] / (self._contour.shape[0] / float(h)))
        symbol = cv2.resize(self._contour, (w, h), interpolation=cv2.INTER_CUBIC)

        if self._margin is None:
            self._margin = int(2 * image.shape[0])

        if self._direction is None:
            self._direction = Direction(random.choice([2, 3]))

        image = cv2.copyMakeBorder(image, 0, 0, self._margin, self._margin, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255, 0))
        coords = get_cut_letter_coords(self._direction, self._margin, image.shape, self._contour_width)
        symbol = fit_image_to_available_area(symbol, self._direction, coords)

        x_offset, y_offset = get_random_offsets(self._direction, coords, symbol)
        image[y_offset + coords[0][1]:y_offset + coords[0][1] + symbol.shape[0], x_offset + coords[0][0]:x_offset + coords[0][0] + symbol.shape[1]] = symbol
        return fit_borders(image)
