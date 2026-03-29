""" Stat info about legacy data. """
import re

from collections import defaultdict
from random import shuffle

from ocr.data.legacy.reader import ocr_samples


def characters(aug="", dates=True, serials=True):
    texts = list(ocr_samples(direction="straight[123]", augmentation=aug, paths_only=True, dates=dates, serials=serials))
    chars = defaultdict(int)

    for image, text in texts:
        for c in text:
            chars[c] += 1

    total_chars = sum(chars.values())
    chars = {c: cnt / total_chars for c, cnt in chars.items()}

    return chars


def containing_chars(aug="", dates=True, serials=True):
    texts = list(ocr_samples(direction="straight[123]", augmentation=aug, paths_only=True, dates=dates, serials=serials))
    has_char = defaultdict(lambda: defaultdict(set))

    for image, text in texts:
        n_chars = 0
        h = hash(image)

        for c in text:
            has_char[c][h].add(text)
            if ord('0') <= ord(c) <= ord('9'):
                has_char["_DIGIT"][h].add(text)
            elif ord('a') <= ord(c) <= ord('z'):
                has_char["_CHAR_LOWER"][h].add(text)
                has_char["_CHAR"][h].add(text)
                n_chars += 1
            elif ord('A') <= ord(c) <= ord('Z'):
                has_char["_CHAR_UPPER"][h].add(text)
                has_char["_CHAR"][h].add(text)
                n_chars += 1
            else:
                has_char["_OTHER"][h].add(text)

        if n_chars == 1:
            has_char["_CHARS_1"][h].add(text)
        elif n_chars == 2:
            has_char["_CHARS_2"][h].add(text)
        elif n_chars >= 3:
            has_char["_CHARS_3+"][h].add(text)

        if 'I' in text and '1' in text:
            has_char["_CONTAIN_I1"][h].add(text)

        if '8' in text and 'B' in text:
            has_char["_CONTAIN_8B"][h].add(text)

        if 'G' in text and '6' in text:
            has_char["_CONTAIN_6G"][h].add(text)

        matches = []

        text_re = re.sub(r"[\W\s_]+", "", text)

        def match(regex):
            if re.match("^" + regex + "$", text_re):
                name = "_RE_" + regex
                name = name.replace("[A-Z]", "a").replace("{2,99}", "++").replace("\\", "").replace("d{2}", "dd").replace("a{2}", "aa")
                # name = name.replace("d++","11").replace("d+","111").replace("d","1").replace("d{2}","dd")
                # name = name.replace("a++","aa").replace("a+","aaa").replace("a","a").replace("a{2}","aa")
                has_char[name][h].add(text)
                matches.append(name)

        match(r"\d+")  # 111111
        match(r"[A-Z]+")  # AAAAAAA

        match(r"[A-Z]\d+")  # A111111111
        match(r"[A-Z]{2,4}\d+")  # AA111111111

        match(r"\d+[A-Z]\d+")  # 111A111
        match(r"\d+[A-Z]{2}\d+")  # 111AA111

        match(r"\d+[A-Z]")  # 1111111A
        match(r"\d+[A-Z]{2}")  # 1111111AA

        match(r"[A-Z]\d+[A-Z]")  # A111A
        match(r"[A-Z]+\d+[A-Z]+")  # AA111AA

        match(r"\w+G\w+")  # xxxGxxx
        match(r"\w+B")  # xxxB
        match(r"\w+8")  # xxx8
        match(r"\w*[A-Z]\w*8")  # xxAxx8

        match(r"\d+B")  # xxxB
        match(r"\d+8")  # xxx8

        match(r"\d\d\d\d\d\d")  # 6 cyfr

        match(r"\d+G\d+")  # same cyfry i G w srodku
        match(r"\d+6\d+")  # same cyfry i 6 w srodku

        if not matches:
            has_char["_RE_OTHER"][h].add(text)
            print("INFO No regex match:", text)

    has_char = {k: (len(v) / len(texts), v.values()) for k, v in has_char.items()}
    for k, (percent, txt) in has_char.items():
        all_values = []
        for v in txt:
            all_values += v
        has_char[k] = (percent, all_values)

    return has_char


def show():
    aug = ""

    def s(dates, serials):
        strings = len(list(ocr_samples(direction="straight[123]", augmentation=aug, paths_only=True, dates=dates, serials=serials)))
        print("Number of strings:", strings)

        stat = characters(aug, dates, serials)
        print("Characters:")
        for char, percent in sorted(stat.items()):
            print(" {char} {percent:.2%}".format(**locals()))

        print("Strings having characters:")
        stat = containing_chars(aug, dates, serials)
        for char, (percent, texts) in sorted(stat.items()):
            texts = list(texts)
            shuffle(texts)
            txt = ""
            for t in texts[:15]:
                txt += "{:<15}".format(t)
            print(" {char:>15} {percent:>8.2%}  {txt}".format(**locals()))

    print("ALL DATA")
    print(s(True, True))

    print()
    print("DATES")
    print(s(True, False))

    print()
    print("SERIALS")
    print(s(False, True))


if __name__ == '__main__':
    show()
