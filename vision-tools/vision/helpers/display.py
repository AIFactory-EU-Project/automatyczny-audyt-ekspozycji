from __future__ import print_function

import os


def set_display_env(force=True):
    if not force and "DISPLAY" in os.environ:
        print("D Using DISPLAY", os.environ["DISPLAY"])
        return
    display_path = os.path.expanduser("~/.lastdisplay")
    if os.path.exists(display_path):
        display = open(display_path).readline().strip()
        print("D Setting DISPLAY env to", display)
        os.environ["DISPLAY"] = display


set_display_env(False)

