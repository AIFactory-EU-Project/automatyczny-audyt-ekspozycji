#!/usr/bin/python2 -O

from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import os
import re

from vision.helpers.showing_progress import showing_progress

DIR_TO_FIX = '/tytan/raid'

os.chdir(DIR_TO_FIX)

print("reading all files...")
with open(DIR_TO_FIX + "/broken_links.txt") as f:
    all_files = sorted([l.strip() for l in f.readlines() if l.strip()])
print("read {} files".format(len(all_files)))

for link in showing_progress(all_files):

    if not os.path.islink(link): continue

    old_target = os.readlink(link)
    new_target = old_target

    new_target = new_target + "/"
    new_target = re.sub(r"\/+", "/", new_target)

    new_target = new_target.replace("/media/nas/vision/", "/tytan/raid/")

    if "/gastro/" in new_target:
        new_target = new_target.replace("/gastro/", "/gastro/")

        new_target = new_target.replace("/aug-3class-", "/augmented/")

        new_target = new_target.replace("/db-", "/databases/")
        new_target = new_target.replace("/db/default_mean", "/databases/default_mean")
        new_target = new_target.replace("/db/emptyfile", "/databases/emptyfile")
        new_target = new_target.replace("/bigval/emptyfile", "/emptyfile")

        new_target = new_target.replace("/gastro/asumayo/", "/gastro/data/asumayo/")
        new_target = new_target.replace("/gastro/cvc/", "/gastro/data/cvc/")
        new_target = new_target.replace("/gastro/cvc-simple/", "/gastro/data/cvc-simple/")
        new_target = new_target.replace("/gastro/cvc-clinic/", "/gastro/data/cvc-clinic/")
        new_target = new_target.replace("/gastro/cvc-clinic-simple/", "/gastro/data/cvc-clinic-simple/")
        new_target = new_target.replace("/gastro/ers/", "/gastro/data/ers/")
        new_target = new_target.replace("/gastro/ers-kapsulki/", "/gastro/data/ers-kapsulki/")
        new_target = new_target.replace("/gastro/ers-simple/", "/gastro/data/ers-simple/")
        new_target = new_target.replace("/gastro/etis-simple/", "/gastro/data/etis-simple/")
        new_target = new_target.replace("/gastro/given/", "/gastro/data/given/")

    new_target = new_target.replace("/./", "/")
    new_target = new_target.replace("/./", "/")

    new_target = re.sub(r"\/+", "/", new_target)
    if new_target.endswith("/"): new_target = new_target[:-1]

    if not os.path.exists(new_target):
        print("WARNING: target does not exist! {} -> {}".format(link, new_target))

    if old_target == new_target:
        # print "Ignoring."
        continue

    stage = 0
    remove_path = link + ".removed"
    try:
        os.rename(link, remove_path)
        stage = 1

        os.symlink(new_target, link)
        stage = 2

        os.unlink(remove_path)
        stage = 3
    except Exception as e:
        print("ERROR!!!", e)

    if stage == 0:
        print("CANNOT MOVE THIS SYMLINK!")
    elif stage == 1:
        print("CANNOT CREATE NEW SYMLINK! Reverting...")
        os.rename(remove_path, link)
    elif stage == 2:
        print("CANNOT REMOVE COPY OF SYMLINK. Ignoring.")
    else:
        pass
        # print "Symlink repaired."

    if stage < 3:
        print("ERROR!!!!!!!!!!!!!!!!")
        print("Reached stage", stage)
        print()
        print("LOC", link)
        print("OLD", old_target)
        print("NEW", new_target)
        break


