from __future__ import unicode_literals, print_function

import pwd
import re
import os
import subprocess
from collections import OrderedDict, defaultdict
from time import sleep
import six
import numpy as np
from datetime import datetime, timedelta



#########################################################
# https://stackoverflow.com/questions/5327707/how-could-i-get-the-user-name-from-a-process-id-in-python-on-linux

UID   = 1
EUID  = 2

def owner(pid):
    '''Return username of UID of process pid'''
    try:
        for ln in open('/proc/{}/status'.format(pid)):
            if ln.startswith('Uid:'):
                uid = int(ln.split()[UID])
                return pwd.getpwuid(uid).pw_name
    except Exception:
        return str(pid)


class GPU(object):
    def __init__(self, id):
        self.id = id
        self.uuid = None
        self.caffe_id = None
        self.name = None
        self.usage = None
        self.processes = None
        self.users = None
        self.memory = None
        self.memory_usage = None
        self.memory_free = None
        self.memory_utilization = None
        self.memory_percent = None
        self.temperature = None

    def __str__(self):
        return "GPU(id:{id}, uuid:{uuid}, caffe:{caffe_id}, name:{name}, usage:{usage}, memory:{memory_usage}/{memory})".format(**vars(self))


def parse(lines):
    lines = list(filter(None, lines))
    data = OrderedDict()
    sections = [data]
    section = data
    for i, line in enumerate(lines):
        line = re.match(r"^( *)(.+?)\s*( : (.*))?$", line)
        level, name, has_value, value = line.groups()
        level = len(level)/4
        while level < len(sections)-1:
            sections.pop()
            section = sections[-1]
        if not has_value or (i < len(lines) - 1 and len(re.match(r"^( *)(.+?)\s*( : (.*))?$", lines[i + 1]).groups()[0]) / 4 > level):  # new section
            new_section = OrderedDict()
            if has_value: name = "{name}:{value}".format(**locals())
            section[name] = new_section
            sections.append(new_section)
            section = new_section
        else:
            section[name] = value
    return data


def read_smi(*args):
    lines = subprocess.check_output(['nvidia-smi', '-q'] + list(args)).decode('utf-8')
    lines = lines.split('\n')
    return parse(lines)


def parse_int(value):
    try:
        return int(value.split(' ')[0])
    except Exception:
        return None


def exact_usage(seconds=10, interval=0.5):
    usage = defaultdict(list)
    starttime = datetime.now()

    while datetime.now() - starttime < timedelta(seconds=seconds):
        for gpu in six.itervalues(gpus()):
            u = gpu.usage if gpu.usage is not None else 50
            usage[gpu.id].append(u)
        sleep(interval)

    result = {}

    for id, usages in six.iteritems(usage):
        result[id] = np.array(usages).mean()

    return result


def gpus():

    data = read_smi()

    gpus_tab = OrderedDict()
    gpu_id = -1
    num_gpus = int(data['Attached GPUs'])

    for section_name, section in six.iteritems(data):
        if section_name.startswith('GPU'):
            gpu_id += 1
            gpu = GPU(gpu_id)
            gpu.uuid = section['GPU UUID']
            gpu.name = section['Product Name']
            if isinstance(section["Processes"], dict):
                gpu.processes = len(section['Processes'])
                pids = [parse_int(p[11:]) for p in section["Processes"]]
                users = {owner(pid) for pid in pids if pid}
                gpu.users = list(users)
            else:
                gpu.processes = parse_int(section['Processes'])
            gpu.memory = parse_int(section['FB Memory Usage']['Total'])
            gpu.memory_usage = parse_int(section['FB Memory Usage']['Used'])
            gpu.memory_free = parse_int(section['FB Memory Usage']['Free'])
            gpu.memory_utilization = parse_int(section['Utilization']['Memory'])
            gpu.memory_percent = 100.0 * gpu.memory_usage / gpu.memory
            gpu.usage = parse_int(section['Utilization']['Gpu'])
            gpu.temperature = parse_int(section['Temperature']['GPU Current Temp'])
            gpu.caffe_id = gpu_id
            gpus_tab[gpu_id] = gpu

    return gpus_tab


def free_gpus(required_memory=0, required_usage=0):
    g = sorted(six.itervalues(gpus()), key=lambda g: (int(0 if g.processes is None else g.processes), -g.memory_free))
    for gpu in g:
        if gpu.usage is None or 100-gpu.usage < required_usage: continue
        if gpu.memory_free is None or gpu.memory_free < required_memory: continue
        yield gpu
    for gpu in g:
        if gpu.usage is None: yield gpu
        elif gpu.memory_free is None: yield gpu


def free_gpu(required_memory=0, required_usage=0):
    gpus = list(free_gpus(required_memory, required_usage))
    if not gpus: raise Exception("There are no free GPUs!")
    else: return gpus[0]


if __name__ == '__main__':
    # from pprint import pprint

    # s = read_smi()
    # for n, s in s.iteritems():
    #     if isinstance(s, dict):
    #         print(n)
    #         for nn, ss in s.iteritems():
    #             print("   ", nn, ss)
    #     else:
    #         print(n, s)

    # for g in gpus().itervalues():
    #     print(g.users)

    print(exact_usage(1))
    for k in free_gpus(required_memory=10000):
        print(k)

