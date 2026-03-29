# coding=utf-8
from __future__ import print_function, unicode_literals

import platform
from datetime import datetime
from io import open
import numpy as np
import six
from six.moves import xrange

from vision.helpers.showing_progress import showing_progress_total, showing_progress_nototal
from vision.helpers.time_helpers import parse_timedelta

FILE = "/tytan/raid/monitor/data.txt"
GROUP = platform.node()
TAG = " "
VALUE = "?"
TIME = '1h'


def _monitor(date_in, date_out, group, tag, value, style="", comment=""):
    try:
        date_in = date_in.strftime("%Y%m%dT%H%M%S")
        date_out = date_out.strftime("%Y%m%dT%H%M%S")
        text = u"{date_in}\t{date_out}\t{group}\t{tag}\t{value}\t{style}\t{comment}\n".format(**locals())
        with open(FILE, 'a') as f:
            f.write(text)
    except Exception as e:
        print("ERROR: {}".format(e))


def monitor(group=None, tag=None, value=None, comment="", time=None, date_in=None, date_out=None, color=None):
    if not group:
        group = GROUP
    if not tag:
        tag = TAG
    if not value:
        value = VALUE
    if not time:
        time = TIME
    if not date_in:
        date_in = datetime.now()
    if not date_out:
        time = parse_timedelta(time.lower())
        date_out = date_in + time
    style = ""
    if color: style += "background-color:{};".format(color)
    _monitor(date_in, date_out, group, tag, value, style, comment)


def percent(group=None, tag=None, value=0, comment="", time=None, color_reversed=False, sign="%"):
    values = list(value) if hasattr(value, '__iter__') else [value]
    values = list(map(lambda v: v*100 if isinstance(v, float) and 0<=v<=1.0 else v, values))
    values = list(map(lambda v: int(round(v)), values))

    value = int(np.array(values).mean().round())

    color = value
    if color > 100: color = 100
    if color < 0: color = 0
    if color_reversed: color = 100-color
    color = (255*(100-color)//100, 255*color//100, 0)
    color = "rgba({},{},{},0.4)".format(*color)

    values = map(lambda v: "{}{}".format(v,sign), values)
    values = u" • ".join(values)

    monitor(group, tag, values, comment, time, color=color)


def monitor_float(group=None, tag=None, value=0, upper_boundary=1e+3, lower_boundary=1e-3, comment="", time=None):
    value = round(value, 6)
    if value > upper_boundary:
        color = 0
    elif value < lower_boundary:
        color = 100
    else:
        lim_min = np.log10(lower_boundary)
        lim_max = np.log10(upper_boundary)
        center = 0.5 * (lim_min + lim_max)
        color = 50 - ((np.log10(value) - center) * 50//abs(lim_min - center))
    color = (int(255 * (100-color)//100), int(255 * color//100))
    color = "rgba({},{},0,0.4)".format(*color)
    monitor(group, tag, "{:.6f}".format(value), comment, time, color=color)


def error(group=None, tag=None, value="ERROR", comment="", time=None):
    monitor(group, tag, value, comment, time, color="rgba(255,0,0,0.4)")


def starting(group=None, tag=None, value="STARTING", comment="", time=None):
    monitor(group, tag, value, comment, time, color="rgba(255,255,0,0.4)")


def working(group=None, tag=None, value="WORKING", comment="", time=None):
    monitor(group, tag, value, comment, time, color="rgba(0,0,255,0.4)")


def finished(group=None, tag=None, value="FINISHED", comment="", time=None):
    monitor(group, tag, value, comment, time, color="rgba(0,255,0,0.4)")


def monitored(iterable, group=None, tag=None, total=None, finish=True):
    if total is None and hasattr(iterable, "__len__"):
        total = len(iterable)

    if total:
        for x in monitored_total(iterable, group, tag, total, finish):
            yield x
    else:
        for x in monitored_nototal(iterable, group, tag, finish):
            yield x


def monitored_total(iterable, group=None, tag=None, total=None, finish=True):
    if total is None: raise ValueError("Total must be set!")
    last = -1
    for i, x in enumerate(showing_progress_total(iterable, total=total)):
        new = i * 100 / total
        if new != last:
            percent(group, tag, new)
            last = new
        yield x

    if finish:
        finished(group, tag)


def monitored_nototal(iterable, group=None, tag=None, finish=True):
    if not group: group = GROUP
    if not tag: tag = TAG
    last = datetime(2000, 1, 1)
    for i, x in enumerate(showing_progress_nototal(iterable, "{group} {tag}: {{counter}}".format(**locals()))):
        if (datetime.now()-last).total_seconds() >= 5:
            monitor(group, tag, i)
            last = datetime.now()
        yield x

    if finish:
        finished(group, tag)


__all__ = ["monitor", "monitor_float", "monitored", "monitored_nototal", "monitored_total", "percent", "error",
           "working", "starting", "finished", "GROUP", "TAG", "VALUE", "TIME"]


if __name__ == "__main__":
    TIME = '1m'
    GROUP = "Test group"

    percent(tag="Test 50", value=50)

    percent(tag="Test 25,75", value=(25,75))
    percent(tag="Test 0,50,100", value=[0,50,100])

    percent(tag="Test 0.25,0.75", value=(0.25,0.75))
    percent(tag="Test 0,0.5,1.0", value=[0,0.5,1.])

    # monitor("Test group", "Test tag", "1%", time=time)
    # monitor("Test group", "Test tag", "10%", time=time)
    # monitor("Test group", "Test tag", "100%", time=time)
    # monitor("Test group", "Test tag 2", "0%", time=time)
    # monitor("Test group", "Test tag 2", "100%", time=time)
    # monitor("Test group 2", "Test tag", "1%", time=time)
    # monitor("Test group 2", "Test tag", "100%", time=time)
    # monitor("Test group 2", "Long tag name long tag name long tag name", "100%", time=time)
    # monitor("Test group 2", "Short tag", "Long tag value long tag value long tag value", color="yellow", time=time)
    # monitor("Very long group name omg wtf szyt", "Test tag", "Test value", time=time)
    # percent("Test group", "Percent", 0, time=time)
    # percent("Test group", "Percent1", 1, time=time)
    # percent("Test group", "Percent10", 10, time=time)
    # percent("Test group", "Percent20", 20, time=time)
    # percent("Test group", "Percent0.5", 0.5, time=time)
    # percent("Test group", "Percent100", 100, time=time)
    # for p in xrange(0,101,10):
    #     percent("Test group", "Percent-{}".format(p), p, time=time)
    # for i in xrange(10000):
    #     monitor("Test group 3", "Many test", i, time=time)
