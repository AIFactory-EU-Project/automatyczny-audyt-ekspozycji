import os
from os import walk
from re import compile


def glob(base_dir, regex, flags=0):
    regex = compile(regex, flags)
    for root, dirs, files in walk(base_dir, followlinks=True):
        for file in files:
            path = root + "/" + file
            if os.name == 'nt':
                path = path.replace("\\", "/")
            match = regex.match(path)
            if match:
                yield path, match.groups()