#!/usr/bin/env python
from __future__ import print_function
import sys
from time import sleep

from vision.monitor.monitor import monitor, percent, working, finished, error


def usage():
    name = "monitor.py"
    print("""\
Usage: {name}          group tag value [time]
       {name} percent  group tag value [time]
       {name} working  group tag       [time]
       {name} finished group tag       [time]
       {name} error    group tag       [time]
       
       time can be: 1h, 10m, 1m30s etc. OR 'permanent' (which means until kill)
       """.format(name=name))


if __name__ == "__main__":
    try:
        args = sys.argv
        args.pop(0)
        operation = args.pop(0) if args[0] in ('percent', 'working', 'finished', 'error') else None
        group = args.pop(0)
        tag = args.pop(0)
        value = args.pop(0) if operation not in ('working', 'finished', 'error') else None
        time = args.pop(0) if args else None
        permanent = time == 'permanent'
        if permanent:
            time = '2m'
        while True:
            if operation == 'percent': percent(group, tag, float(value), time=time)
            elif operation == 'working': working(group, tag, time=time)
            elif operation == 'finished': finished(group, tag, time=time)
            elif operation == 'error': error(group, tag, time=time)
            else: monitor(group, tag, value, time=time)
            if permanent:
                sleep(60)
            else:
                break
    except Exception as e:
        usage()
        exit(1)
