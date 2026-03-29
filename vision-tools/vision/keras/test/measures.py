import numpy as np


# measures from https://en.wikipedia.org/wiki/F1_score
def multilabel_measures(ground_truth, predictions, threshold=0.5, mean_result=True):
    measures = {}

    ground_truth = np.array(ground_truth, dtype=np.uint8)
    predictions = np.array(np.array(predictions) >= threshold, dtype=np.uint8)
    tp = np.float32(np.sum(np.logical_and(ground_truth == 1, predictions == 1), axis=0))
    fp = np.float32(np.sum(np.logical_and(ground_truth == 0, predictions == 1), axis=0))
    tn = np.float32(np.sum(np.logical_and(ground_truth == 0, predictions == 0), axis=0))
    fn = np.float32(np.sum(np.logical_and(ground_truth == 1, predictions == 0), axis=0))

    with np.errstate(divide='ignore', invalid='ignore'):
        measures["prevalence"] = np.nan_to_num((tp + fn) / (tp + tn + fp + fn))
        measures["accuracy"] = np.nan_to_num((tp + tn) / (tp + tn + fp + fn))
        measures["precision"] = measures["ppv"] = np.nan_to_num(tp / (tp + fp))
        measures["fdr"] = np.nan_to_num(fp / (tp + fp))
        measures["for"] = np.nan_to_num(fn / (tn + fn))
        measures["npv"] = np.nan_to_num(tn / (tn + fn))
        measures["recall"] = measures["sensitivity"] = measures["tpr"] = np.nan_to_num(tp / (tp + fn))
        measures["fallout"] = measures["fpr"] = np.nan_to_num(fp / (tn + fp))
        measures["fnr"] = np.nan_to_num(fn / (tp + fn))
        measures["specificity"] = measures["tnr"] = np.nan_to_num(tn / (tn + fp))
        measures["lr+"] = np.nan_to_num(measures['tpr'] / measures['fpr'])
        measures["lr-"] = np.nan_to_num(measures['fnr'] / measures['tnr'])
        measures["dor"] = np.nan_to_num(measures['lr+'] / measures['lr-'])
        measures["fscore"] = np.nan_to_num(2 * measures["precision"] * measures["recall"] / (measures["precision"] + measures["recall"]))
        measures["fscore_ss"] = np.nan_to_num(2 * measures["sensitivity"] * measures["specificity"] / (measures["sensitivity"] + measures["specificity"]))
        measures["accuracy_whole"] = np.float32(np.nan_to_num(np.sum(np.all(predictions == ground_truth, axis=1)) / predictions.shape[0]))
        measures["empty"] = np.float32(np.nan_to_num(1 - np.count_nonzero(np.sum(predictions, axis=1)) / predictions.shape[0]))

    if mean_result:
        for k, v in measures.items():
            measures[k] = v.mean()

    return measures


def multiclass_measures(ground_truth, predictions):
    indices = np.argmax(predictions, axis=1)
    predictions = np.zeros_like(predictions, dtype=np.uint8)
    predictions[np.arange(predictions.shape[0]), indices] = 1
    return multilabel_measures(ground_truth, predictions)


def regression_measures(ground_truth, predictions, mean_result=True):
    measures = {}

    with np.errstate(divide='ignore', invalid='ignore'):
        measures["distance"] = np.absolute(ground_truth - predictions)
        measures["relative_error"] = np.nan_to_num(measures["distance"] / ground_truth)
        measures["accuracy"] = np.float32(np.nan_to_num(np.sum(np.all(predictions == ground_truth, axis=1)) / predictions.shape[0]))

    if mean_result:
        for k, v in measures.items():
            measures[k] = v.mean()

    return measures