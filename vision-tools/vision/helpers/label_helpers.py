import json
import os
from collections import OrderedDict

import six


def save_labels(labels, path):
    with open(path, "w") as f:
        s = json.dumps(labels, f, sort_keys=True)
        s = s.replace("], ", "],\n\t")
        s = s.replace("{", "{\n\t")
        s = s.replace("}", "\n}")
        f.write(s)


def save_labels_txt(labels, path, sort=False, append=False):
    labels_txt_lines = []
    pairs = six.iteritems(labels) if isinstance(labels, dict) else labels

    if sort:
        pairs = sorted(pairs)

    for imgpath, label in pairs:
        if isinstance(label, list) or isinstance(label, tuple):
            label = " ".join([str(x) for x in label])
        labels_txt_lines.append("{imgpath} {label}".format(**locals()))

    mode = "a" if append else "w"
    with open(path, mode) as f:
        for line in labels_txt_lines:
            f.write(line + "\n")
            

def save_labels_json_dict(labels, path):
    with open(path, "w") as f:
        json.dump(labels, f)


def change_directory(labels, new_dir):
    """ Returns loaded labels with changed directory. Does not save! """
    pairs = six.iteritems(labels) if isinstance(labels, dict) else labels
    pairs = [(os.path.join(new_dir, os.path.basename(imgpath)), label) for imgpath, label in pairs]
    return OrderedDict(pairs) if isinstance(labels, dict) else pairs


def get_data_type(label, as_string=False):
    numtype = str
    if as_string:
        return numtype

    try:
        int(label)
        numtype = int
    except ValueError:
        try:
            float(label)
            numtype = float
        except ValueError:
            pass

    return numtype


def load_labels_txt_dict(path, as_string=False):
    labels_list = load_labels_txt_list(path, as_string)
    labels = OrderedDict(labels_list)
    return labels


def load_labels_json_dict(path):
    with open(path) as data_file:
        data = json.load(data_file)
    return data


def load_labels_txt_list(path, as_string=False):
    with open(path, "r") as f:
        lines = f.read().splitlines()

    labels = []
    if len(lines) == 0:
        return labels

    first_label = lines[0].split(None, 1)[1].split()[0]
    numtype = get_data_type(first_label, as_string)

    for line in lines:
        if line == "":
            continue
        path, label_str = line.split(None, 1)
        label_split_str = label_str.split()
        label = [numtype(x) for x in label_split_str]
        if len(label) == 1:
            label = label[0]
        path = path.replace("//", "/")
        labels.append((path, label))

    return labels


def save_names_txt(names, path):
    with open(path, "w") as f:
        f.write("\n".join(names))


def load_names_txt(path):
    lines = open(path).readlines()
    names = [l.strip().split()[0] for l in lines]
    names = list(filter(lambda n: n.find(":") == -1, names))
    return names


def single_to_one_hot(names, label):
    one_hot = [0] * len(names)
    one_hot[label] = 1
    return one_hot


def one_hot_to_single(label):
    for i, v in enumerate(label):
        if v:
            return i


def labels_single_to_one_hot(names, labels):
    one_hot_labels = []
    for path, label in labels:
        entry = (path, single_to_one_hot(names, label))
        one_hot_labels.append(entry)
    return one_hot_labels


def has_one_label(labels):
    return sum(map(int, labels)) == 1
