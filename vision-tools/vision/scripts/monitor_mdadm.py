import platform
import subprocess
import time
from datetime import timedelta, datetime

from vision.monitor import monitor


class Raid(object):
    def __init__(self, device):
        self.device = device
        self.status = None
        self.level = None
        self.devices = None
        self.reshape_percent = None
        self.reshape_time = None

    def __repr__(self):
        return "RAID {device} {level} {status} devices: {devices2} reshape: {reshape_time} {reshape_percent}".format(devices2=" ".join(self.devices), **vars(self))


def read_mdadm():
    raid = None
    for line in open("/proc/mdstat"):
        line = line.strip()
        if not line: continue
        line = line.split()
        if len(line) < 3: continue
        if line[0].startswith("md"):
            if raid: yield raid
            device, _, status, level = line[:4]
            devices = line[4:]
            devices = map(lambda d: d[:-3], devices)
            raid = Raid(device)
            raid.status = status
            raid.level = level
            raid.devices = devices
        elif raid and line[1] == 'reshape':
            raid.reshape_percent = float(line[3][:-1])*0.01
            raid.reshape_time = timedelta(minutes=float(line[5][7:-3]))
    if raid: yield raid



if __name__ == '__main__':
    monitor.GROUP = "Raid"
    while True:
        for raid in read_mdadm():
            if raid.reshape_percent:
                tag = platform.node() + " " + raid.device
                fin_time = datetime.now() + raid.reshape_time
                fin_time = "Finish: " + fin_time.strftime("%Y-%m-%d %H:%M")
                print raid
                print fin_time
                monitor.percent(tag=tag, value=raid.reshape_percent, comment=fin_time)

        time.sleep(60)
