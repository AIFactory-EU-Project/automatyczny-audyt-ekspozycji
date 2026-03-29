import cv2
import json
import numpy as np
import os

from vision.keras.models.networks import GeneralNeuralNetwork
from vision.metrics.numpy import multilabel
from vision.tensorflow.gpus import tensorflow_use_gpus


def test_meals(src_dir, show=False):
    tensorflow_use_gpus(1)
    with open("/tytan/raid/shelf-retail/data/classification/mapping.json") as f:
        class_data = json.load(f)
        class_names = [name for name, label in sorted(class_data.items(), key=lambda item: item[1])]

    test_labels_path = os.path.join(src_dir, "labels.json")
    classes = len(class_names)
    weights_path = "/tytan/raid/shelf-retail/models/classification/resnext/v3/2020-01-17 17:59:46/model-123-0.19.hdf5"
    img_size = (224, 224, 3)
    pad_image = True
    grayscale = False
    net = "resnext"
    activation = "sigmoid"
    thresholds = 0.5

    network_params = (weights_path, classes, img_size, pad_image, grayscale, net, activation)
    network = GeneralNeuralNetwork(*network_params)

    gt = []
    rd = []
    labels = json.load(open(test_labels_path))
    for path, gt_labels in labels.items():
        img = cv2.imread(path)
        predictions = network.predict([img])[0]
        pred = np.array(predictions >= thresholds, dtype=np.float32())

        gt_vec = np.zeros([classes])
        for label in gt_labels:
            mapped_label = class_data.get(label, 0)
            np.put(gt_vec, mapped_label, 1)

        # handle Unknown class
        positives = np.count_nonzero(pred == 1)
        if (pred == 0).all() or (positives == 1 and pred[-1] == 1):
            np.put(pred, 0, 1)

        if show:
            msg = ""
            for i, a in enumerate(pred):
                if a:
                    msg += "{:>2d} {:1.2f} {}\n ".format(i, predictions[i], class_names[i])
            if not msg:
                msg = "---"

            print(msg)
            cv2.imshow("img", img)
            cv2.waitKey()

        gt.append(gt_vec)
        rd.append(pred)

    rd = np.array(rd)
    gt = np.array(gt)

    from tensorflow import Session
    from vision.keras.train import metrics
    f1_score = metrics.f1_score_spec(gt, rd).eval(session=Session())

    print("ACCURACY")
    print(multilabel.accuracy(rd, gt))
    print("F1 SCORE")
    print(f1_score)
    print(multilabel.f1score_spec(rd, gt))

    f1score_spec_per_class = multilabel.f1score_spec(rd, gt, per_class=True).tolist()
    for name, score in list(zip(class_names, f1score_spec_per_class)):
        print(name, score)


if __name__ == '__main__':
    test_meals("/tytan/raid/shelf-retail/data/classification/v05/test/", show=False)
