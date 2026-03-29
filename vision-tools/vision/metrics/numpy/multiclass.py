import re
import itertools

import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib
import matplotlib.pyplot as plt
from textwrap import wrap


def plot_confusion_matrix(gt, prediction, labels, normalize=False):
    """
    Prepares confusion matrix figure.

    Source: https://stackoverflow.com/questions/41617463/tensorflow-confusion-matrix-in-tensorboard

    :param gt: ground truth
    :param prediction: predicted scores
    :param labels: class names
    :param normalize: normalization improves CM coloring for
    :return: pyplot figure
    """
    cm = confusion_matrix(gt.argmax(axis=1), prediction.argmax(axis=1), labels=range(len(labels)))
    cm_normalized = cm.astype('float') * 100 / cm.sum(axis=1)[:, np.newaxis]
    cm_normalized = np.nan_to_num(cm_normalized, copy=True)
    cm_normalized = cm_normalized.astype('int')
    if normalize:
        cm = cm_normalized

    np.set_printoptions(precision=2)

    fig = plt.Figure(figsize=(7, 7), dpi=320, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(cm_normalized, cmap='Blues')

    # Wrap long class names
    classes = [re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', x) for x in labels]
    classes = ['\n'.join(wrap(l, 40)) for l in classes]

    tick_marks = np.arange(len(classes))

    ax.set_xlabel('Predicted', fontsize=7)
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(classes, fontsize=4, rotation=-90, ha='center')
    ax.xaxis.set_label_position('bottom')
    ax.xaxis.tick_bottom()

    ax.set_ylabel('True Label', fontsize=7)
    ax.set_yticks(tick_marks)
    ax.set_yticklabels(classes, fontsize=4, va='center')
    ax.yaxis.set_label_position('left')
    ax.yaxis.tick_left()

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax.text(j, i, format(cm[i, j], 'd') if cm[i, j] != 0 else '.', horizontalalignment="center", fontsize=6,
                verticalalignment='center', color="black")
    fig.set_tight_layout(True)

    # Attach a new canvas if not exists
    if fig.canvas is None:
        matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
    fig.canvas.draw()

    return fig
