""" Load sentences from .txt files. """
import random
import os
import codecs

from ocr.aug.aug_utils import Singleton


class TemplateLoader:
    __metaclass__ = Singleton

    def __init__(self, mode):
        if mode == "serial_number":
            mode = "serial"

        current_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        with codecs.open(os.path.join(current_dir, mode + ".txt"), encoding="utf-8") as f:
            self.expressions = f.readlines()

    def get_random_expr(self):
        return random.choice(self.expressions).rstrip()


if __name__ == "__main__":
    for _ in range(100):
        print(TemplateLoader("serial").get_random_expr())
