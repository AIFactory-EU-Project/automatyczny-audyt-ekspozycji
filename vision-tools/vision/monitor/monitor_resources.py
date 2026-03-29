#!/usr/bin/python2
# coding=utf-8
import os
import platform
import psutil
from collections import namedtuple, defaultdict

import six

from vision.monitor.monitor import percent, monitor
from vision.helpers import gpu

#######################################################################################
# source: http://stackoverflow.com/a/42249349
def cpu_usage_():
    usage = float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline())
    usage = int(round(usage))
    return usage


#######################################################################################
# source: http://stackoverflow.com/a/7285509
_ntuple_diskusage = namedtuple('usage', 'total used free')
def disk_usage_(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _ntuple_diskusage(total, used, free)


#######################################################################################
# cpu_temp

sensors_init = False

def cpu_temp():
    try:
        global sensors_init

        import sensors

        if not sensors_init:
            sensors.init()

        temps = [0]
        for chip in sensors.iter_detected_chips():
            for feature in chip:
                try:
                    if "temp" in feature.label.lower() or "temp" in chip.prefix.lower():
                        temps.append(int(round(float(feature.get_value()))))
                except Exception:
                    pass
        return max(temps)

    except Exception:
        return None


#######################################################################################
# using psutil

def cpu_usage():

    for p in psutil.process_iter():
        p.cpu_percent()

    total = psutil.cpu_percent(10)

    users = defaultdict(float)

    for p in psutil.process_iter():
        users[p.username()] += p.cpu_percent()

    users = {k:v for k,v in six.iteritems(users) if v >= 15}
    return total, users


def memory_usage():
    return psutil.virtual_memory().percent


def disk_usage(path):
    usage = psutil.disk_usage(path)
    return usage.total, usage.used, usage.free


def monitor_disks():
    host = platform.node()

    if host == 'tytan': disks = [("Tytan raid", "/tytan/raid/"), ("Tytan storage", "/tytan/storage/"), ("NAS", "/media/nas/")]
    elif host == 'kolos': disks = [("Kolos M.2", "/kolos/m2/"), ("Kolos SSD", "/kolos/ssd/"), ("Kolos storage", "/kolos/storage/"), ("NAS", "/media/nas/")]
    elif host == 'atlas': disks = [("Atlas SSD", "/")]
    # elif host == 'jachoocta': disks = [("jachoo SSD", "/"), ("jachoo HDD", "/storage/"), ("NAS", "/media/nas/")]
    # else: disks = [(host, "/")]
    else: disks = []

    for name, path in disks:
        if not os.path.exists(path) or not os.path.isdir(path): continue
        total, used, free = disk_usage(path)
        free /= 1024.**3
        monitor("Disks", name, "{:.1f} GB".format(free), time='10m')


def monitor_resources():
    group = platform.node()

    cpu, cpu_users = cpu_usage()
    cpu_users = "Users: " + ", ".join("{} ({:.0f}%)".format(u,v) for u,v in six.iteritems(cpu_users))

    memory = memory_usage()

    percent(group, u"CPU • RAM", (cpu,memory), time='5m', color_reversed=True, comment=cpu_users)

    gpus = gpu.gpus()
    usages = gpu.exact_usage()

    for id, usage in six.iteritems(usages):
        if usage is None: continue
        usage = int(round(usage))
        users = gpus[id].users
        if users: users = "Users: " + ",".join(users)
        else: users = ""
        memory = gpus[id].memory_percent
        percent(group, u"GPU {} • RAM".format(id), (usage,memory), time='5m', color_reversed=True, comment=users)

    gpu_t = max(gpu.temperature for gpu in six.itervalues(gpus))
    cpu_t = cpu_temp()
    percent("Temperatures", group, (cpu_t, gpu_t), color_reversed=True, sign="*C")



if __name__ == "__main__":
    monitor_resources()
    monitor_disks()
