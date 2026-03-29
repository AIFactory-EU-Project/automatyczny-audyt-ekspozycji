import numpy as np
import sklearn.metrics

"""
Multilabel classification metrics
"""


def accuracy(prediction, gt, threshold=0.5, per_class=False):
    """
    Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    tps, tns, fps, fns = confusion_matrix(prediction, gt, threshold)
    acc = 1.0 * (tps + tns) / (tps + tns + fps + fns)
    if per_class:
        return acc
    return acc.mean()


def sensitivity(prediction, gt, threshold=0.5, per_class=False, allow_nan=False):
    """
    Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    tps, tns, fps, fns = confusion_matrix(prediction, gt, threshold)
    with np.errstate(divide='ignore', invalid='ignore'):
        sens = tps / (tps + fns)
        if not allow_nan: sens = np.nan_to_num(sens)
    if per_class:
        return sens
    return sens.mean()


def specificity(prediction, gt, threshold=0.5, per_class=False, allow_nan=False):
    """
    Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    tps, tns, fps, fns = confusion_matrix(prediction, gt, threshold)
    with np.errstate(divide='ignore', invalid='ignore'):
        spec = tns / (tns + fps)
        if not allow_nan: spec = np.nan_to_num(spec)
    if per_class:
        return spec
    return spec.mean()


def precision(prediction, gt, threshold=0.5, per_class=False):
    """
    Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    tps, tns, fps, fns = confusion_matrix(prediction, gt, threshold)
    with np.errstate(divide='ignore', invalid='ignore'):
        prec = np.nan_to_num(tps / (tps + fps))
    if per_class:
        return prec
    return prec.mean()


def recall(prediction, gt, threshold=0.5, per_class=False):
    """
    Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.
    """
    return sensitivity(prediction, gt, threshold, per_class)


def f1score(prediction, gt, threshold=0.5, per_class=False, beta=1.0):
    """
    Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.
    """
    prec = precision(prediction, gt, threshold, per_class=True)
    rec = recall(prediction, gt, threshold, per_class=True)
    with np.errstate(divide='ignore', invalid='ignore'):
        f1 = np.nan_to_num((1. + (beta ** 2)) * prec * rec / ((beta ** 2) * prec + rec))
    if per_class:
        return f1
    return f1.mean()


def f1score_spec(prediction, gt, threshold=0.5, per_class=False, nan_as_one=False):
    """
    Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.
    """
    sens = sensitivity(prediction, gt, threshold, per_class=True, allow_nan=True)
    spec = specificity(prediction, gt, threshold, per_class=True, allow_nan=True)
    beta = 1.0
    with np.errstate(divide='ignore', invalid='ignore'):
        f1 = (1. + (beta ** 2)) * sens * spec / ((beta ** 2) * spec + sens)
        if nan_as_one:
            f1[np.isnan(f1)] = 1
            f1[np.isinf(f1)] = 1
        f1 = np.nan_to_num(f1)
    if per_class:
        return f1
    return f1.mean()


def confusion_matrix(prediction, gt, threshold=0.5):
    """
    Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    tps = np.float32(sum(np.logical_and(gt == 1.0, prediction >= threshold)))
    fns = np.float32(sum(np.logical_and(gt == 1.0, prediction < threshold)))
    tns = np.float32(sum(np.logical_and(gt == 0.0, prediction < threshold)))
    fps = np.float32(sum(np.logical_and(gt == 0.0, prediction >= threshold)))
    return tps, tns, fps, fns


def roc_auc(prediction, gt, *args, **kwargs):
    """
    Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    num_classes = gt.shape[-1]
    aucs = []
    for i in range(num_classes):
        # if there's only one class in gt, return 0 instead of raising an error
        if len(np.unique(gt[:, i])) == 1:
            auc = 0.
        else:
            auc = sklearn.metrics.roc_auc_score(gt[:, i], prediction[:, i])
        aucs.append(auc)
    return np.array(aucs)


def max_threshold(prediction, gt, metric):
    """Thresholds for metric maximization"""
    max_metric = np.zeros((prediction.shape[1]))
    max_metric_threshold = np.zeros((prediction.shape[1]))
    for threshold in np.linspace(0.01, 1, 100):
        curr_metric = metric(prediction, gt, threshold, per_class=True)
        for i in range(0, prediction.shape[1]):
            if curr_metric[i] > max_metric[i]:
                max_metric[i] = curr_metric[i]
                max_metric_threshold[i] = threshold

    return max_metric_threshold


def max_threshold_with_margin(prediction, gt, metric, margin):
    """
    Find threshold optimizing given metric value, while also being as close to 0.5 as possible.
    Metric value for the chosen threshold cannot be lower than (max_value - margin).
    Returns lists of thresholds (one for each class).
    """

    thresholds = np.linspace(0.01, 1, 100)
    all_metrics = []
    for threshold in thresholds:
        all_metrics.append(metric(prediction, gt, threshold, per_class=True))
    all_metrics = np.stack(all_metrics)

    best_thresholds = []
    for i in range(all_metrics.shape[1]):
        cls_metrics = all_metrics[:, i]
        valid_thresholds = thresholds[cls_metrics >= max(cls_metrics) - margin]
        best_threshold = valid_thresholds[np.argmin(np.abs(valid_thresholds - 0.5))]
        best_thresholds.append(best_threshold)

    return np.asarray(best_thresholds)


def recall_for_precision(prediction, gt, precision_th):
    recalls = []

    for cls_pred, cls_gt in zip(prediction.T, gt.T):
        precision, recall, _ = sklearn.metrics.precision_recall_curve(cls_gt, cls_pred)
        for idx, prec in enumerate(precision):
            if prec >= precision_th:
                break
        recalls.append(recall[idx])

    return recalls


def sensitivity_for_specificity(prediction, gt, spec_th):
    tprs = []
    thresholds = []

    for cls_pred, cls_gt in zip(prediction.T, gt.T):
        # tpr = recall = sensitivity
        fpr, tpr, ths = sklearn.metrics.roc_curve(cls_gt, cls_pred)
        specificity = 1 - fpr
        for idx, spec in enumerate(specificity):
            if spec <= spec_th:
                break
        tprs.append(tpr[idx])
        thresholds.append(ths[idx])

    return tprs, thresholds


def roc_curve(prediction, gt):
    """Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.

    :return tpr: true positive rate (sensitivity), array of shape (?, class_count)
    :return fpr: false positive rate (1-specificity), array of shape (?, class_count)
    """
    prediction, gt = _preprocess(prediction, gt)
    num_classes = gt.shape[-1]

    tpr = []
    fpr = []
    for i in range(num_classes):
        if len(np.unique(gt[:, i])) == 1:
            tpr.append(np.array([])), fpr.append(np.array([]))
            continue

        fpr_i, tpr_i, _ = sklearn.metrics.roc_curve(y_true=gt[:, i], y_score=prediction[:, i])
        tpr.append(tpr_i), fpr.append(fpr_i)

    return tpr, fpr


def pr_curve(prediction, gt):
    """Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.

    :return prec: precision array of shape (?, class_count)
    :return rec: recall (sensitivity, true positive rate) array of shape (?, class_count)
    """
    prediction, gt = _preprocess(prediction, gt)
    num_classes = gt.shape[-1]

    prec = []
    rec = []
    for i in range(num_classes):
        if len(np.unique(gt[:, i])) == 1:
            prec.append(np.array([])), rec.append(np.array([]))
            continue

        prec_i, rec_i, _ = sklearn.metrics.precision_recall_curve(y_true=gt[:, i], probas_pred=prediction[:, i])
        prec.append(prec_i), rec.append(rec_i)

    return prec, rec


def average_precision_score(prediction, gt):
    """
    Expects arrays of shape: (batch, class_count). Array will be squeezed to handle single element dimensions.
    """
    prediction, gt = _preprocess(prediction, gt)
    num_classes = gt.shape[-1]

    aps = []
    for i in range(num_classes):
        # if there's only one class in gt, return 0 instead of raising an error
        if len(np.unique(gt[:, i])) == 1:
            ap = 0.
        else:
            ap = sklearn.metrics.average_precision_score(gt[:, i], prediction[:, i])
        aps.append(ap)

    return np.array(aps)


def _preprocess(prediction, gt):
    if prediction.ndim > 2:
        prediction = np.squeeze(prediction)
    if gt.ndim > 2:
        gt = np.squeeze(gt)
    return prediction, gt
