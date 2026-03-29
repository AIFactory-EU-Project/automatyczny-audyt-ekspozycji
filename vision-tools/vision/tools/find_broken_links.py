#!/usr/bin/python2 -O

from __future__ import print_function
import os

from vision.helpers.showing_progress import showing_progress

DIR_TO_FIX = '/tytan/raid'

os.chdir(DIR_TO_FIX)

print("reading all files...")
with open(DIR_TO_FIX + "/symlinks.txt") as f:
    all_files = sorted([l.strip() for l in f.readlines() if l.strip()])
print("read {} files".format(len(all_files)))

outfile = open(DIR_TO_FIX + "/broken_links.txt", 'w')

for link in showing_progress(all_files):
    if "_OUT_" in link: continue
    if not os.path.islink(link): continue
    if not os.path.exists(link):
        # print link
        outfile.write(link.strip()+ "\n")

outfile.close()



