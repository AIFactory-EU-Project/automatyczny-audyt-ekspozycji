""" Load distributions from real data:
    - dotted / normal / embossed proportions
    - probability of character occurrences
"""
import json
import random
import os
from math import log

from ocr.data.legacy.reader import ocr_samples
from ocr.data.legacy.stats import containing_chars, characters
from ocr.aug.config import config
from vision.aug.utils import weighted_choice


class DistributionConfig:
    def __init__(self):
        dist_data = None
        if os.path.exists(config.aug.distribution_path):
            with open(config.aug.distribution_path, "r") as f:
                dist_data = json.load(f)

        if dist_data:
            self.serial_chars_dict = dist_data["serials_characters"]
            self.dates_chars_dict = dist_data["dates_characters"]
            self.dates_containing_chars_dict = dist_data["dates_containing_chars"]
            self.font_types = dist_data["font_types"]

            self.serial_alpha_characters_dict = {
                key: self.serial_chars_dict[key]
                for key in self.serial_chars_dict if key.isalpha()}
            self.serial_numeric_characters_dict = {
                key: self.serial_chars_dict[key]
                for key in self.serial_chars_dict if key.isdigit()}
        else:
            self.serial_chars_dict = characters(dates=False, serials=True)
            self.dates_chars_dict = characters(dates=True, serials=False)
            self.font_types = self.distribution_of_font_types()
            self.serial_alpha_characters_dict = {
                key: self.serial_chars_dict[key]
                for key in self.serial_chars_dict if key.isalpha()}

            self.serial_numeric_characters_dict = {
                key: self.serial_chars_dict[key]
                for key in self.serial_chars_dict if key.isdigit()}

            self.dates_containing_chars_dict = \
                {key: value for key, (value, _) in containing_chars(dates=True, serials=False).items()}

            self.dates_containing_chars_dict = {
                key: value for key, value in self.dates_containing_chars_dict.items()
                if key in [" ", "/", "-", ".", "\\", ":", ""]}

            probability_sum = sum(v for k, v in self.dates_containing_chars_dict.items())
            self.dates_containing_chars_dict[""] = 1 - probability_sum

            self.serial_chars_dict = self.transform_distribution(self.serial_chars_dict)
            self.serial_alpha_characters_dict = self.transform_distribution(self.serial_alpha_characters_dict)
            self.serial_numeric_characters_dict = self.transform_distribution(self.serial_numeric_characters_dict)
            self.dates_containing_chars_dict = self.transform_distribution(self.dates_containing_chars_dict)

            self.save_distribution()

    @staticmethod
    def size_of_dataset(font, direction="straight*"):
        return len(list(ocr_samples(paths_only=True, direction=direction, font=font))) / 2

    def distribution_of_font_types(self):
        total = self.size_of_dataset(font="*", direction="straight*")
        return {
            "dotted": self.size_of_dataset(font="dotted", direction="straight*") / float(total),
            "normal": self.size_of_dataset(font="normal", direction="straight*") / float(total),
            "embossed": self.size_of_dataset(font="embossed", direction="straight*") / float(total)
        }

    @staticmethod
    def transform_distribution(distribution):
        log_base = 2

        def transform_func(x):
            result = (log(x)/log(log_base))
            return result

        coeff = log_base/min(distribution.values())
        for key, value in distribution.items():
            distribution[key] = transform_func(coeff*value)

        probability_sum = sum(v for k, v in distribution.items())

        for key, value in distribution.items():
            distribution[key] = value/float(probability_sum)

        return distribution

    def save_distribution(self):
        distribution_info = {
            "serials_characters": self.serial_chars_dict,
            "dates_characters": self.dates_chars_dict,
            "dates_containing_chars": self.dates_containing_chars_dict,
            "font_types": self.font_types
        }
        with open(config.aug.distribution_path, "w") as f:
            json.dump(distribution_info, f)

    @staticmethod
    def distribution_stats(distribution_dict):
        total = 0
        for key, value in distribution_dict.items():
            total += value

        print(total)

    @staticmethod
    def weighted_choice(choices_dict, probability_sum=None):
        return weighted_choice(choices_dict, probability_sum)

    def get_date_separator(self):
        separator = self.weighted_choice(
            self.dates_containing_chars_dict)
        # TODO - consider if wide spaces are needed

        return separator if separator != " " else "   "

    def get_long_date_format(self):
        separator = self.get_date_separator()
        formats = [
            "{{0}}{}{{1}}{}{{2}}",
            "{{1}}{}{{0}}{}{{2}}",
        ]

        return random.choice(formats).format(separator, separator)

    def get_short_date_format(self):
        separator = self.get_date_separator()
        formats = [
            "{{0}}{}{{1}}",
            "{{1}}{}{{0}}",
        ]

        return random.choice(formats).format(separator, separator)

    def get_serial_number_char(self):
        return self.weighted_choice(self.serial_chars_dict)

    def get_serial_number_alpha_char(self):
        return self.weighted_choice(self.serial_alpha_characters_dict)

    def get_serial_number_numeric_char(self):
        return self.weighted_choice(self.serial_numeric_characters_dict)

    def get_font_type(self):
        return self.weighted_choice(self.font_types)


if __name__ == "__main__":
    dist_config = DistributionConfig()
