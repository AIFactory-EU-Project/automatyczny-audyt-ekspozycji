import logging
import re

from numpy import mean
from datetime import date, datetime

from ocr.scanner.worker import Worker
from vision.helpers.box_helpers import bb_intersection_over_union


class TextParser(Worker):
    """ Process for post-processing results: computes best results from given Frames. """
    def __init__(self, queue):
        super(TextParser, self).__init__("parser", outputs=queue)
        self.year_prefix = ""
        self.date_regex = ""
        self.serial_regex = ""
        self.serial_regexes = ""
        self.sequence_regex = ""

    def init(self):
        self.year_prefix = "20"
        # EXP, koncem, waznosci or before
        self.date_regex = r".*" \
                          r"(([EF][XKY][PR])" \
                          r"|(K[O0][NM]CE[MN])" \
                          r"|(WAZ[NM][O0]SC[Il1])" \
                          r"|(BEF[O0]RE))" \
                          r"[)]?[:*]?[ ]?([0-9* ]+)"

        self.serial_regex = r".*" \
                            r"((L[O0]T)" \
                            r"|(SER[IL]{2})" \
                            r"|(PART[IL]{2})" \
                            r"|(SER[IL]A)" \
                            r"|([B8].[ ]?[NM][O0].)" \
                            r"|(C[YX][JI][NM][E][JI]))" \
                            r"[)]?[:*]?[ ]?" \
                            r"((\d+)" \
                            r"|([A-Z]\d+)" \
                            r"|([A-Z]{2,4}\d+)" \
                            r"|(\d+[A-Z]\d+)" \
                            r"|(\d+[A-Z]{2}\d+)" \
                            r"|(\d+[A-Z])" \
                            r"|(\d+[A-Z]{2})" \
                            r"|([A-Z]\d+[A-Z])" \
                            r"|([A-Z]+\d+[A-Z]+))"

        self.sequence_regex = r"([A-Z]|[0-9])\1{2,}"
        self.serial_regexes = [r"\d+", r"[A-Z]\d+", r"[A-Z]{2,4}\d+", r"\d+[A-Z]\d+", r"\d+[A-Z]{2}\d+", r"\d+[A-Z]", r"\d+[A-Z]{2}", r"[A-Z]\d+[A-Z]", r"[A-Z]+\d+[A-Z]+"]

    def process(self, data):
        box = data
        box.barcode = self.extract_barcode(box)
        box.date, box.date_score, box.serial_number, box.serial_number_score = self.extract_fields(box)
        box.time = datetime.now() - box.one_frame().timestamp
        logging.debug("DATE: {}".format(box.date))
        logging.debug("SERIAL: {}".format(box.serial_number))
        return box

    @staticmethod
    def extract_barcode(box):
        if len(box.frames) == 0:
            return ""
        codes = [frame.barcode.text for _, box_frames in box.frames.items() for frame in box_frames]
        codes.sort(key=lambda x: len(x), reverse=True)

        return codes[0]

    @staticmethod
    def validate_date_values(year, month, day=None):
        if day:
            if day < "01" or day > "31":
                return False
        if month < "01" or month > "12":
            return False
        if year < "2000" or year > "2100":
            return False
        return True

    def validate_candidates(self, candidates):
        validate = []
        for cand in candidates:
            if self.validate_date_values(*cand):
                cand = list(map(int, cand))
                validate.append(cand)
        return validate

    def parse_4_format(self, first_part, sec_part):
        # required format is 10/17
        if len(first_part) != 2:
            return None
        if first_part > "12":
            # if both numbers are larger than 12, return None date
            if sec_part > "12":
                return None
            return date(int(self.year_prefix + first_part), int(sec_part), day=1)
        else:
            return date(int(self.year_prefix + sec_part), int(first_part), day=1)

    @staticmethod
    def get_closest_date(validate):
        curr_date = datetime.today().date()
        intervals = []
        for v in validate:
            # full date format
            if len(v) == 3:
                v_date = date(*v)
            else:
                v_date = date(*v, day=1)
            intervals.append((abs(curr_date - v_date).days, v_date))

        # get the most probable candidate (the one closest to current date)
        return min(intervals)[1]

    def parse_date(self, ocr_date):
        ocr_date = ocr_date.replace(" ", "")
        splitted = ocr_date.split("*")
        # longest possible format is 20*10*2017
        if len(splitted) > 3:
            return None
        parsed_date = None

        # no "*" found
        if len(splitted) == 1:
            date_length = len(ocr_date)
            if date_length == 4:
                parsed_date = self.parse_4_format(ocr_date[:2], ocr_date[2:])

            if date_length == 6:
                # candidates for date (possible formats: 2017.10, 10.2017)
                candidates = [(ocr_date[:4], ocr_date[4:]),
                              (ocr_date[2:], ocr_date[:2])]
                validate = self.validate_candidates(candidates)
                # proper candidate not found
                if not validate:
                    return None
                parsed_date = self.get_closest_date(validate)

            if date_length == 8:
                # candidates for date (possible formats: 20.10.2017, 2017.10.20)
                candidates = [(ocr_date[4:], ocr_date[2:4], ocr_date[:2]),
                              (ocr_date[:4], ocr_date[4:6], ocr_date[6:])]
                validate = self.validate_candidates(candidates)
                # proper candidate not found
                if not validate:
                    return None
                parsed_date = date(*validate[0])
        else:
            improper = [True for part in splitted if not part]
            if improper:
                return None
            date_length = len("".join(splitted))

            if date_length == 4:
                parsed_date = self.parse_4_format(*splitted)

            if date_length == 6:
                # 2017*10 or 10*2017 format
                if len(splitted) == 2:
                    # swap places so year is first
                    if len(splitted[0]) != 4:
                        splitted[0], splitted[1] = splitted[1], splitted[0]
                    if self.validate_date_values(*splitted):
                        splitted = [int(part) for part in splitted]
                        parsed_date = date(*splitted, day=1)

            if date_length == 8:
                if len(splitted) == 3:
                    # swap places so year is first
                    if len(splitted[0]) != 4:
                        splitted[0], splitted[2] = splitted[2], splitted[0]
                    if self.validate_date_values(*splitted):
                        splitted = [int(part) for part in splitted]
                        parsed_date = date(*splitted)

        return parsed_date

    def check_if_candidate(self, text, letters=False):
        text_copy = text
        if not letters:
            return self.parse_date(text_copy)
        return None

    @staticmethod
    def get_date_conf(date):
        curr_date = datetime.today().date()
        delta = abs(curr_date - date).days
        # dates which has more than 1 year of difference from now
        if delta > 360:
            return 0.4
        return -0.5 * delta / 360 + 0.9

    @staticmethod
    def get_distance_conf(dist):
        if dist > 50:
            return 0.5
        return -0.5 * dist / 50 + 0.9

    @staticmethod
    def check_lists(dates, serials):
        if not dates:
            if not serials:
                return "", 1.0, "", 1.0
            else:
                serials.sort(key=lambda x: x[1], reverse=True)
                best = serials[0]
                return "", 1.0, best[0], best[1]
        elif not serials:
            dates.sort(key=lambda x: x[1], reverse=True)
            best = dates[0]
            return best[0], best[1], "", 1.0
        else:
            return None

    def calculate_distance_based_conf(self, dates, serials):
        improper = self.check_lists(dates, serials)
        if improper:
            return improper
        results = []
        for t, s, (x_min, y_min, x_max, y_max) in dates:
            for t2, s2, (x_min2, y_min2, x_max2, y_max2) in serials:
                if t == t2:
                    continue
                if bb_intersection_over_union((x_min, y_min, x_max, y_max), (x_min2, y_min2, x_max2, y_max2)) > 0.5:
                    continue
                conf = max(self.get_distance_conf(abs(x_min - x_min2)), self.get_distance_conf(abs(y_min - y_min2)))
                results.append((t, s, t2, mean([s2, conf])))
        return results if results else [("", 1.0, "", 1.0)]

    def deal_with_date(self, date_candidate, text, conf, pos, res_dates, res_serials):
        serial_conf = mean([conf, 0.1])
        # date confidence increases while it"s closer to current date
        date_conf = mean([conf, self.get_date_conf(date_candidate)])
        res_dates.append((text, date_conf, pos))
        res_serials.append((text, serial_conf, pos))

    def deal_with_serial(self, text, conf, pos, res_serials):
        # serial numbers cannot contain lowercase letters
        if any([c.islower() for c in text]):
            pass
        serial_conf = mean([conf, 0.7])
        # higher confidence for serials matching regexes
        if any([re.match(reg, text) for reg in self.serial_regexes]):
            serial_conf = mean([conf, 0.9])
        # lower confidence for special characters or short serials
        if "*" in text or len(text) == 3:
            serial_conf = mean([conf, 0.4])
        res_serials.append((text, serial_conf, pos))

    def extract_fields(self, box):
        if len(box.frames) == 0:
            return "", 1.0, "", 1.0

        best_pairs = []
        detections = [frame.detections for _, box_frames in box.frames.items() for frame in box_frames]
        for detection_group in detections:
            best_detections = [d for d in detection_group if len(d.text) > 2 and d.confidence > 0.5]
            possible_dates = []
            possible_serials = []
            # only one region detected
            if len(best_detections) == 1:
                d = best_detections[0]
                return d.text, d.confidence, d.text, d.confidence
            for detection in best_detections:
                text, conf = detection.text, detection.confidence
                pos = detection.x1, detection.y1, detection.x2, detection.y2
                text_len = len(text)
                letters = sum([c.isalpha() for c in text])
                letters_dominating = float(letters) / text_len >= 0.5
                match_date = None
                match_serial = None
                # try to extract date/serial number from long string
                if text_len > 8:
                    match_date = re.match(self.date_regex, text, flags=re.IGNORECASE)
                    match_serial = re.match(self.serial_regex, text, flags=re.IGNORECASE)
                # too many letters indicates that it"s neither date nor serial number
                if letters_dominating and not (match_date or match_serial):
                    continue

                # it can be date as well as serial number (but for most cases it would be date)
                date_candidate = self.check_if_candidate(text, letters)
                if date_candidate:
                    self.deal_with_date(date_candidate, text, conf, pos, possible_dates, possible_serials)
                else:
                    self.deal_with_serial(text, conf, pos, possible_serials)

                if match_date:
                    d_text = match_date.group(6)
                    date_candidate = self.check_if_candidate(d_text)
                    if date_candidate:
                        self.deal_with_date(date_candidate, d_text, conf, pos, possible_dates, possible_serials)

                if match_serial:
                    s_texts = set([s for i, s in enumerate(match_serial.groups()) if i > 6 and s])
                    for s_text in s_texts:
                        self.deal_with_serial(s_text, conf, pos, possible_serials)

            improper = self.check_lists(possible_dates, possible_serials)
            if improper:
                best_pairs.append(improper)
                continue
            possible_serials.sort(key=lambda x: x[1], reverse=True)
            best = possible_serials[0]
            pairs = []
            for text, score, _ in possible_dates:
                pairs.append((text, score, best[0], best[1]))
            pairs.sort(key=lambda x: x[1] + x[3], reverse=True)
            best_pairs.append(pairs[0])
            # updated_pairs = self.calculate_distance_based_conf(possible_dates, possible_serials)
            # updated_pairs.sort(key=lambda x: x[1] + x[3], reverse=True)
            # best_pairs.append(updated_pairs[0])

        # return best pair among all frames
        best_pairs.sort(key=lambda x: x[1] + x[3], reverse=True)
        return best_pairs[0]
