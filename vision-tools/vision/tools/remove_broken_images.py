#!/usr/bin/env python2

import os
import sys

import cv2 as cv

from vision.helpers.file_helpers import all_files

FILE_OK = 0
FILE_NOT_FOUND = 1
FILE_IS_DIR = 2
FILE_OTHER_TYPE = 3
FILE_CANNOT_READ = 4


def check_file(file):
    if not os.path.exists(file): return FILE_NOT_FOUND
    if os.path.isdir(file): return FILE_IS_DIR
    _, ext = os.path.splitext(file)
    if not ext: return FILE_OTHER_TYPE

    ext = ext.lower()[1:]
    if ext in ('jpg', 'png', 'jpeg', 'bmp', 'gif', 'tif', 'tiff'):
        img = cv.imread(file)
        if img is None or not img.shape or not img.shape[0] or not img.shape[1]:
            img = cv.imread(file)
        if img is None or not img.shape or not img.shape[0] or not img.shape[1]:
            return FILE_CANNOT_READ
        else:
            return FILE_OK

    #TODO: pliki wideo

    return FILE_OTHER_TYPE


def remove_file_and_dirs(path):
    os.remove(path)
    try:
        while True:
            path = os.path.dirname(path)
            os.rmdir(path)
    except OSError:
        pass


def find_broken_images(filelist):
    for file in filelist:
        check = check_file(file)
        if check == FILE_CANNOT_READ:
            yield file


def remove_broken_images(filelist_or_dir):
    if isinstance(filelist_or_dir, (str, unicode)):
        filelist = all_files(filelist_or_dir)
    else:
        filelist = filelist_or_dir

    broken = find_broken_images(filelist)

    for file in broken:
        print("Removing: {}".format(file))
        remove_file_and_dirs(file)


def remove_broken_labels(labels_file):
    repaired_file = "{labels_file}.repaired".format(**locals())
    backup_file = "{labels_file}.backup".format(**locals())

    print("Repairing {labels_file} to {repaired_file}".format(**locals()))

    with open(repaired_file, 'w') as output, open(labels_file) as input:
        for line in input:
            line = line.strip()
            if not line: continue
            path = line.split(" ")[0]
            if check_file(path) != FILE_OK:
                print("Removing {}".format(path))
                remove_file_and_dirs(path)
            else:
                output.write(line + "\n")

    print("Backuping to {backup_file}".format(**locals()))
    os.rename(labels_file, "{labels_file}.backup".format(**locals()))

    print("Saving back to {labels_file}".format(**locals()))
    os.rename(repaired_file, labels_file)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dirs = sys.argv[1:]
    else:
        dirs = [os.getcwdu()]

    for d in dirs:
        print("Checking {}".format(d))
        if os.path.isdir(d):
            remove_broken_images(d)
        else:
            remove_broken_labels(d)

