# coding=utf-8
from __future__ import print_function, unicode_literals

import platform
import subprocess as sp
import time
from datetime import timedelta, datetime

from vision.monitor import monitor


class Sensor(object):
    def __init__(self, device, temperature=None):
        self.device = device
        self.temperature = temperature

    def __repr__(self):
        return "TEMP {device} {temperature}".format(**vars(self))


def read_sensors():
    for line in sp.check_output("sensors").splitlines():
        line = line.decode("utf-8")

        line = line.strip()
        if not line: continue

        if ":" not in line: continue
        if "°C" not in line: continue

        name = line[:line.index(":")]
        temp = line[line.index(":")+1:]
        temp = temp.split()[0]

        temp = temp[:-2]
        temp = float(temp)

        yield Sensor(name, temp)



if __name__ == '__main__':
    monitor.GROUP = "Temperature"
    while True:
        for sensor in read_sensors():
            print(sensor.device, sensor.temperature)
        print()

        time.sleep(1)
