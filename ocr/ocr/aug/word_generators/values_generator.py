""" Generate strings. """
from __future__ import print_function

import logging
import random
import codecs
import time
import re

from ocr.aug.base_words.loader import TemplateLoader
from ocr.aug.aug_utils import Singleton
from ocr.aug.config import config
from ocr.aug.distribution import DistributionConfig


class config(config):
    class probability(config.aug):
        date = .1
        serial = .1
        numeric = .1
        template_sentence = .1
        serial_from_reg_exp = 85.
        random_serial = 1. - serial_from_reg_exp

    class dummy(config.aug):
        max_length = 50
        min_length = 3


DUMMY_TEXT_SEPARATORS = {
    " ": 0.9,
    "/": 0.01,
    "_": 0.01,
    "*": 0.01,
    ";": 0.01,
    ",": 0.01,
    ":": 0.01,
    "-": 0.01,
    "%": 0.01,
    ".": 0.01,
    "+": 0.01
}

SERIAL_NUMBER_SPECIAL_CHARS = "./: _-"

DUMMY_TEXT_ALLOWED_CHARACTERS = "aąbcćdeęfghijklłmnńoóprqsśtuwvxyzźż" + \
                                "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRQSŚTUWVXYZŹŻ" + \
                                ',\"?*;"%+°' + \
                                '0123456789' + \
                                SERIAL_NUMBER_SPECIAL_CHARS


class TextValueGenerator(object):
    __metaclass__ = Singleton
    distribution = DistributionConfig()
    SERIAL_LENGTH = (4, config.params.max_serial_number_length)

    def __init__(self):
        self.check_sum(DUMMY_TEXT_SEPARATORS)
        with codecs.open(config.aug.dict_path, "r", encoding="utf-8") as f:
            self.lines = f.readlines()
        logging.info(f"Dictionary {config.aug.dict_path} loaded")
        self.string_from_exp_generator = StringFromRegExpGenerator(self.distribution)

    @staticmethod
    def check_sum(dictionary):
        sum = 0
        for _, value in dictionary.items():
            sum += value

        assert sum == 1

    def get_random_word(self):
        while True:
            word = random.choice(random.choice(self.lines).split(" ")).rstrip().lstrip().replace(",", "")
            if all(c.isalpha() for c in word) and all(c in DUMMY_TEXT_ALLOWED_CHARACTERS for c in word) and word != " ":
                return word

    @staticmethod
    def get_numeric_word():
        start_chars = ["nr", "numer", "numer pozwolenia", "pozwolenie numer"]
        short_end_chars = ["mg", "%", "ml", "mg/ml", u"°", u"°C", "g", "m", "cm", "mm", "kg"]
        long_end_chars = [u" kapsułek", " tabletek", " saszetek", u" kapsułki", " tabletki", " saszetki"]

        value = str(random.choice([random.randint(0, 10000), round(random.uniform(0., 10000.), 2)]))

        if random.random() < .9:
            if random.random() < .25:
                if random.getrandbits(1):
                    value += random.choice([" ", ""]) + random.choice(short_end_chars)
                else:
                    value += random.choice(long_end_chars)
            else:
                value = random.choice(start_chars) + random.choice([" ", ": "]) + value

        return value

    @staticmethod
    def str_time_prop(start, end, format, prop):
        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))
        ptime = stime + prop * (etime - stime)

        return time.strftime(format, time.localtime(ptime))

    def get_date_value(self):
        if random.random() < 0.95:
            date_format = self.distribution.get_short_date_format()
            template = date_format.format("%m", "%Y")
            start = date_format.format(1, 2017)
            end = date_format.format(1, 2030)
        else:
            date_format = self.distribution.get_long_date_format()
            template = date_format.format("%m", "%d", "%Y")
            start = date_format.format(1, 1, 2017)
            end = date_format.format(1, 1, 2030)

        return self.str_time_prop(start, end, template, random.random())

    def get_serial_number_from_reg_exp(self, length=None):
        return self.string_from_exp_generator.get_random_string(length)

    def get_random_serial_number(self, length=None):
        special = SERIAL_NUMBER_SPECIAL_CHARS
        value = ""
        for i in range(length):
            random_char = self.distribution.get_serial_number_char()
            while random_char in special and (i in [0, length - 1] or value[-1] in special):
                random_char = self.distribution.get_serial_number_char()
            value += random_char

        return value

    def get_serial_number_value(self, length=None):
        if length is None:
            length = random.randint(*self.SERIAL_LENGTH)

        if random.random() < config.probability.serial_from_reg_exp:
            value = self.get_serial_number_from_reg_exp(length)
        else:
            value = self.get_random_serial_number(length)

        return value

    def get_date_template(self):
        return TemplateLoader("date").get_random_expr() + " " + self.get_date_value()

    def get_serial_template(self):
        return TemplateLoader("serial").get_random_expr() + " " + self.get_serial_number_value()

    def get_random_dict_sentence(self):
        length_in_words = random.randint(1, 3)
        sentence = ""
        for i in range(length_in_words):
            if random.random() < config.probability.numeric:
                sentence += self.get_numeric_word() + " "
                continue

            if random.random() < config.probability.template_sentence:
                sentence += random.choice([self.get_date_template, self.get_serial_template])() + " "
                break

            choice = DistributionConfig.weighted_choice(DUMMY_TEXT_SEPARATORS)
            word = self.get_random_word()
            sentence += word + choice \
                if choice == " "  \
                else word + random.choice(["", " "]) + choice + random.choice(["", " "])

        sentence = sentence[0].upper() + sentence[1:]
        sentence = sentence[:-1] + "."

        return sentence

    def get_possibly_cropped_dict_sentence(self):
        probability_of_crop = .2
        while True:
            sentence = self.get_random_dict_sentence()
            if random.random() < probability_of_crop:
                text_length = len(sentence)
                max_cut = int(0.1 * text_length)
                left = random.randint(0, max_cut)
                right = random.randint(0, max_cut)

                sentence = sentence[right:-left]

            if any(c.isalpha() for c in sentence):
                return sentence

    def get_dummy_text(self):
        while True:
            sentence = self.get_possibly_cropped_dict_sentence()
            if random.random() < config.probability.date:
                sentence += " " + self.get_date_value()
            elif random.random() < config.probability.serial:
                sentence += " " + self.get_serial_number_value()

            if config.dummy.min_length < len(sentence) < config.dummy.max_length:
                return sentence

    def dict_stats(self):
        unallowed = u""
        for line in self.lines:
            for char in line:
                if char not in DUMMY_TEXT_ALLOWED_CHARACTERS:
                    if char not in unallowed:
                        unallowed += char
        print("Unallowed characters: " + unallowed)

    def generator_stats(self):
        unallowed = u""
        for _ in range(10000):
            for char in self.get_dummy_text():
                if char not in DUMMY_TEXT_ALLOWED_CHARACTERS:
                    if char not in unallowed:
                        unallowed += char
        print("Unallowed characters: " + unallowed)

        lengths = []
        for i in range(1000):
            text = TextValueGenerator().get_dummy_text()
            print(u"{}\t{}".format(len(text), text))
            lengths.append(len(text))

        print("Average length: {}".format(sum(lengths)/float(len(lengths))))
        print("Max length: {}".format(max(lengths)))
        print("Min length: {}".format(min(lengths)))


class StringFromRegExpGenerator:
    """ String generator from simplified regular expressions """
    expressions = [
        r"\d+",             # 111111
        r"[A-Z]\d+",        # A111111111
        r"[A-Z]{2,4}\d+",   # AA111111111
        r"\d+[A-Z]\d+",     # 111A111
        r"\d+[A-Z]{2}\d+",  # 111AA111
        r"\d+[A-Z]",        # 1111111A
        r"\d+[A-Z]{2}",     # 1111111AA
        r"[A-Z]\d+[A-Z]",   # A111A
        r"[A-Z]+\d+[A-Z]+"  # AA111AA

        r"\w+G\w+",         # xxxGxxx
        r"\w+B",            # xxxB
        r"\w+8",            # xxx8
        r"\d+B",            # xxxB
        r"\d+8",            # xxx8
        r"\w*[A-Z]\w*8",
        r"\d+G\d+",         # same cyfry i G w srodku
        r"\d+6\d+"          # same cyfry i 6 w srodku
    ]

    def __init__(self, distribution):
        self.distribution = distribution

    def get_random_string(self, length):
        reg_exp = random.choice(self.expressions)
        return self.get_value(reg_exp, length)

    def get_value(self, reg_exp, length):
        char_dict = {}

        for m in re.finditer("\[A-Z]", reg_exp):
            char_dict[m.start()] = "alpha", self.get_occurrences_limiter(reg_exp, m.start() + 5)

        indexes = [i for i, c in enumerate(reg_exp) if c.isupper() and c not in ["A", "Z"]]
        indexes.extend([i for i, c in enumerate(reg_exp) if c.isdigit() and c not in ["2", "4"]])

        for index in indexes:
            char_dict[index] = reg_exp[index], 1

        for m in re.finditer("\\\d", reg_exp):
            char_dict[m.start()] = "numeric", self.get_occurrences_limiter(reg_exp, m.start() + 2)

        for m in re.finditer("\\\w", reg_exp):
            char_dict[m.start()] = "alphanumeric", self.get_occurrences_limiter(reg_exp, m.start() + 2)

        # get max length of unlimited substrings
        max_length = length
        number_of_unlimited_substrings = 0
        for _, value in char_dict.items():
            char_type, occurrences = value
            if occurrences is not None:
                max_length -= occurrences
            else:
                number_of_unlimited_substrings += 1

        # find values for fixed-size substrings
        for key in sorted(char_dict):
            char_type, occurrences = char_dict[key]
            if occurrences is None:
                continue
            if char_type not in ["alpha", "numeric", "alphanumeric"]:
                char_dict[key] = char_type, char_type
                continue

            char_dict[key] = char_type, self.get_fixed_size_substring(char_type, occurrences)

        # find values for unlimited substrings
        substring_lengths = list(self.random_ints_with_sum(max_length, number_of_unlimited_substrings))

        counter = 0
        serial_number_value = ""
        for key in sorted(char_dict):
            char_type, occurrences = char_dict[key]
            if occurrences is None:
                serial_number_value += self.get_fixed_size_substring(char_type, substring_lengths[counter])
                counter += 1
            else:
                serial_number_value += occurrences

        return serial_number_value

    @staticmethod
    def random_ints_with_sum(sum, n):
        """ Generate non-negative n random integers summing to `sum`. """
        for i in range(n):
            if i == n - 1:
                yield sum
            elif sum > 0:
                r = random.randint(0, sum)
                yield r
                sum -= r
            else:
                yield 0

    def get_fixed_size_substring(self, chars_type, length):
        value = ""
        for _ in range(length):
            if chars_type == "numeric":
                value += self.distribution.get_serial_number_numeric_char()

            if chars_type == "alpha":
                value += self.distribution.get_serial_number_alpha_char()

            if chars_type == "alphanumeric":
                if random.random() < .5:
                    value += self.distribution.get_serial_number_alpha_char()
                else:
                    value += self.distribution.get_serial_number_numeric_char()

        return value

    @staticmethod
    def get_occurrences_limiter(text, position):
        try:
            if text[position] == "+":
                return None
            elif text[position] == "{":
                position_end = position
                while text[position_end] != "}":
                    position_end += 1

                limiters = text[position+1:position_end].replace(" ", "").split(",")[:2]
                if len(limiters) == 1:
                    return int(limiters[0])
                elif len(limiters) == 2:

                    return random.randint(int(limiters[0]), int(limiters[1]))
                else:
                    assert len(limiters) in [1, 2]
            else:
                return 1

        except IndexError:
            return 1


def main():
    for _ in range(0, 10):
        print(TextValueGenerator().get_serial_number_value())


if __name__ == "__main__":
    main()
