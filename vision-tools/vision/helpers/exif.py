"""
Sets orientation in file exif metadata to a given value.

If run as main, it takes two arguments - [orientation] and [directory] - and processes all files within given directory.
E.g.
/usr/bin/python3.5 set_exif_orientation.py 1 /home/username/folder-with-images/
"""

import piexif
import sys
import os

from datetime import datetime


def set_exif_orientation(file_name, orientation):
    """
    Sets orientation in file exif metadata to a given value.
    Note: no value range check is done.

    :param file_name: File to be modified.
    :param orientation: Value to be set.
    :return: Nothing
    """

    try:
        exif_dict = piexif.load(file_name)
        exif_dict["0th"][piexif.ImageIFD.Orientation] = orientation
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, file_name)
    except Exception as error:
        print("Error occurred when processing {0}: {1}".format(file_name, error))


def get_exif_time(file_name):
    """
    Gets time from exif data.

    :param file_name: File to get time
    :return: Time image was taken
    """
    time = None
    try:
        exif_dict = piexif.load(file_name)
        time = exif_dict["0th"][piexif.ImageIFD.DateTime]
    except Exception as error:
        print("Error occurred when processing {0}: {1}".format(file_name, error))

    return datetime.strptime(time.decode("utf-8"), "%Y:%m:%d %H:%M:%S") if time is not None else None


if __name__ == "__main__":
    try:
        orientation = int(sys.argv[1])
        directory = sys.argv[2]
    except (IndexError, ValueError):
        print("Please provide two valid parameters: [orientation] [directory]")
        sys.exit()

    print("Starting execution")
    for file in os.listdir(directory):
        processed_file = os.path.join(directory, file)
        set_exif_orientation(processed_file, orientation)
    print("Finished processing")
