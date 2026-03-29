# -*- coding: utf-8 -*-

###############################################################################
# This software and source code is proprietary and confidential.
#
# Unauthorized using, copying, distributing, sharing or modifying of this file,
# via any medium and for any purpose is strictly prohibited.
#
# Authors & rights owners:
#
# Adam Brzeski <brzeski@eti.pg.gda.pl>
# Jan Cychnerski <jan.cychnerski@eti.pg.gda.pl>
#
# Copyright (C) 2013-2016 All Rights Reserved
###############################################################################

import importlib
import os
import traceback


def available_modules(dir_or_file):
    if os.path.isfile(dir_or_file):
        dir = os.path.dirname(os.path.realpath(dir_or_file))
    else:
        dir = os.path.realpath(dir_or_file)
    modules = []
    for entry in os.listdir(dir):
        if entry == '__init__.py':
            continue
        if entry[-3:] == ".py":
            entry = entry[:-3]
        elif not os.path.isdir(dir + "/" + entry):
            continue
        if os.path.isdir(dir + "/" + entry) and not os.path.exists(dir + "/" + entry + "/__init__.py"):
            continue
        modules.append(entry)
    return modules


def load_modules(modules, package, priority=None, do_print=False):
    if priority is None: priority = {}
    for module in sorted(modules, key=lambda m: priority.get(m, m)):
        try:
            if do_print: print("Loading module: {package}.{module}".format(**locals()), end=' ')
            importlib.import_module(package + "." + module)
        except BaseException as e:
            print("ERROR during loading module:", module)
            print(e)
            if __debug__:
                traceback.print_exc()
