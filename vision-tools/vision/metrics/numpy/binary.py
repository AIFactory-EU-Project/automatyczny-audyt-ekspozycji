import numpy as np
import sklearn.metrics


"""
Binary classification metrics
"""


def accuracy(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    tp, tn, fp, fn = confusion_matrix(prediction, gt, threshold)
    acc = 1.0 * (tp + tn) / (tp + tn + fp + fn)
    return acc


def sensitivity(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    tp, tn, fp, fn = confusion_matrix(prediction, gt, threshold)
    sens = 1.0 * tp / (tp + fn) if tp + fn != 0 else 0
    return sens


def specificity(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    tp, tn, fp, fn = confusion_matrix(prediction, gt, threshold)
    spec = 1.0 * tn / (tn + fp) if tn + fp != 0 else 0
    return spec


def precision(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    tp, tn, fp, fn = confusion_matrix(prediction, gt, threshold)
    prec = 1.0 * tp / (tp + fp) if tp + fp != 0 else 0
    return prec


def recall(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    return sensitivity(prediction, gt, threshold)


def f1score(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    prec = precision(prediction, gt, threshold)
    rec = recall(prediction, gt, threshold)
    f1 = (2.0 * prec * rec) / (prec + rec) if prec + rec != 0 else 0
    return f1


def f1score_spec(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    sens = sensitivity(prediction, gt, threshold)
    spec = specificity(prediction, gt, threshold)
    f1 = (2.0 * sens * spec) / (sens + spec) if sens + spec != 0 else 0
    return f1


def confusion_matrix(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    tp = true_positive(prediction, gt, threshold)
    tn = true_negative(prediction, gt, threshold)
    fp = false_positive(prediction, gt, threshold)
    fn = false_negative(prediction, gt, threshold)
    return tp, tn, fp, fn


def true_positive(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    prediction = np.uint8(prediction > threshold)
    return np.sum(np.logical_and(gt == 1, prediction == 1))


def true_negative(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    prediction = np.uint8(prediction > threshold)
    return np.sum(np.logical_and(gt == 0, prediction == 0))


def false_positive(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    prediction = np.uint8(prediction > threshold)
    return np.sum(np.logical_and(gt == 0, prediction == 1))


def false_negative(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    prediction = np.uint8(prediction > threshold)
    return np.sum(np.logical_and(gt == 1, prediction == 0))


def roc_auc(prediction, gt, *args, **kwargs):
    """
    Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    auc = sklearn.metrics.roc_auc_score(gt, prediction)
    return auc


def best_fscore_spec_thresh(prediction, gt):
    """Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.

    :return int: threshold for best f1 score spec
    """
    prediction, gt = _preprocess(prediction, gt)

    max_fscore = 0
    max_fscore_threshold = 0
    thresholds = []
    for threshold in np.linspace(0.01, 1, 100):
        curr_fscore = f1score_spec(prediction, gt, threshold)
        if curr_fscore > max_fscore:
            max_fscore = curr_fscore
            max_fscore_threshold = threshold
        thresholds.append(threshold)

    return max_fscore_threshold


def roc_curve(prediction, gt):
    """Expects arrays of shape: (batch) or (batch, 2). Array will be squeezed to handle single element dimensions.

    :return tpr: true positive rate (sensitivity) array of unknown shape.
    :return fpr: false positive rate (1-specificity) array of unknown shape.
    """
    prediction, gt = _preprocess(prediction, gt)

    fpr, tpr, _ = sklearn.metrics.roc_curve(y_true=gt, y_score=prediction)

    return tpr, fpr


def pr_curve(prediction, gt):
    """Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.

    :return prec: precision array of unknown shape.
    :return rec: recall (sensitivity, true positive rate) array of unknown shape.
    """
    prediction, gt = _preprocess(prediction, gt)

    prec, rec, _ = sklearn.metrics.precision_recall_curve(y_true=gt, probas_pred=prediction)

    return prec, rec


def _preprocess(prediction, gt):
    prediction = np.squeeze(prediction)
    gt = np.squeeze(gt)

    # Convert categorical to binary if required (in case binary clf is trained as 2-class multiclass)
    if len(prediction.shape) > 1 and prediction.shape[1] == 2:
        prediction = prediction[:, 1]
    if len(gt.shape) > 1 and gt.shape[1] == 2:
        gt = np.argmax(gt, axis=1)

    return prediction, gt
