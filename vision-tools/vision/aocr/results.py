#!/usr/bin/python2 -O

from __future__ import print_function

from functools import total_ordering
from glob import iglob
from pprint import pprint

import os

import six
import tensorflow as tf
from collections import defaultdict

# todo need refactor


def all_events(base_dir):
    events_name = "events.out.tfevents.*"
    for file in iglob(base_dir + "/" + events_name):
        yield file
    for file in iglob(base_dir + "/*/" + events_name):
        yield file
    for file in iglob(base_dir + "/*/*/" + events_name):
        yield file


def all_data(base_dir):
    print("DEBUG: Reading all data from", base_dir)
    results = {}
    for events in all_events(base_dir):
        try:
            result = results[events] = defaultdict(dict)
            for event in tf.train.summary_iterator(events):
                step = event.step
#                if step < 200000: continue
                time = event.wall_time
                for tagvalue in event.summary.value:
                    tag, value = tagvalue.tag, tagvalue.simple_value
                    if step in result and tag in result[step]:
                        raise Exception("Data already in set")
                    result[step][tag] = value
        except Exception as e:
            print("ERROR:", e)
    return results


def all_tests(base_dir):
    data = all_data(base_dir)
    print("DEBUG: Filtering data...")
    tests = {}
    for events, steps in six.iteritems(data):
        test = tests[events] = {}
        test_steps = set()
        for step, tags in six.iteritems(steps):
            for tag, value in six.iteritems(tags):
                if "test" in tag:
                    test_steps.add(step)
        for step, tags in six.iteritems(steps):
            if step not in test_steps: continue
            test[step] = tags
    return tests


def select_best(data):

    @total_ordering
    class Result(object):
        def __init__(self, path, step, tags, value):
            self.path = path
            self.step = step
            self.tags = tags
            self.value = value

        def __cmp__(self, other):
            if self.value < other.value: return -1
            elif self.value > other.value: return 1
            else: return 0

        def __le__(self, other):
            return self.__cmp__(other) < 0

        def __eq__(self, other):
            return self.__cmp__(other) == 0

        def __repr__(self):
            return "Result(step={self.step},value={self.value},path={self.path},tags={self.tags})".format(self=self)


    values = defaultdict(list)

    for path, steps in six.iteritems(data):
        for step, tags in six.iteritems(steps):
            for tag, value in six.iteritems(tags):
                if "hyperparams" in tag: continue
                val = Result(path, step, tags, value)
                values[tag].append(val)

    print("INFO: best values")
    for tag, results in six.iteritems(values):

        print()
        print("INFO: tag", tag)

        results.sort()
        if "loss" not in tag and "gradient" not in tag: results.reverse()

        for result in results:
            model_dir = os.path.normpath(result.path + "/../..")
            checkpoint = model_dir + "/model.ckpt-{}".format(result.step)
            if not os.path.exists(checkpoint + ".meta"):
                print("WARN: checkpoint file deleted:", result)
                continue
            print("INFO:", checkpoint, result)
            break


if __name__ == '__main__':
    import sys

    if len(sys.argv) >= 2:
        directory = sys.argv[1]
    else:
        from .boxes_aocr.config_boxes import config
        directory = config.boxes.all_chars_updown.model_dir

    data = all_tests(directory)
    select_best(data)


