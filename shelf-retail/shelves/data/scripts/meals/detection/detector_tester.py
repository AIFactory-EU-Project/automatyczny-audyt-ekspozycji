from collections import defaultdict

import json
import os

import cv2
import mmcv
import numpy as np
from mmcv.parallel import MMDataParallel
from mmcv.runner import load_checkpoint
from mmdet.apis import inference_detector, init_dist
from mmdet.models import build_detector

from vision.tensorflow.detection.testing import detector_tester as tester

SRC_PATH = "/tytan/raid/shelf-retail/data/detection/meals/v02/annotations/validation.json"
CFG_PATH = "../../../../models/detection/meals/cascade_mask_rcnn_r4_gcb_dconv_c3-c5_x101_32x4d_fpn_syncbn_1x.py"
CKPT_PATH = "/tytan/raid/shelf-retail/models/detection/meals/v2/cascade_mask_rcnn_r4_gcb_dconv_c3-c5_x101_32x4d_fpn_syncbn_1x/latest.pth"


def test(src_dir, cfg_path, ckpt_path, show=True):
    """
    Verify trained model on a test set.

    :param src_dir: A path to the test directory.
    :param cfg_path: A path to the trained model's config file.
    :param ckpt_path: A path to the trained model's checkpoint file.
    """
    if 'RANK' not in os.environ:
        os.environ['RANK'] = str(0)
    if 'WORLD_SIZE' not in os.environ:
        os.environ['WORLD_SIZE'] = str(1)
    if 'MASTER_ADDR' not in os.environ:
        os.environ['MASTER_ADDR'] = '192.168.44.100'
    if 'MASTER_PORT' not in os.environ:
        os.environ['MASTER_PORT'] = str(8522)

    cfg = mmcv.Config.fromfile(cfg_path)
    model = build_detector(
        cfg.model, train_cfg=None, test_cfg=cfg.test_cfg)
    load_checkpoint(model, ckpt_path)
    init_dist("pytorch", **cfg.dist_params)

    model = MMDataParallel(model, device_ids=[0])
    model.cfg = cfg

    with open(src_dir) as f:
        json_data = json.load(f)

    data_dict = defaultdict(list)
    for img_data in json_data["images"]:
        for anno_data in json_data["annotations"]:
            if anno_data["image_id"] == img_data["id"]:
                img_pth = os.path.join(os.path.dirname(os.path.dirname(src_dir)), os.path.basename(src_dir).split(".")[0], img_data["file_name"])
                data_dict[img_pth].append(anno_data["bbox"])

    final_results = {
        "meals": {
            "class": {"tp": 0, "fp": 0, "fn": 0},
            "boxes": []
        },
    }

    for img_pth, annotations in data_dict.items():
        result = inference_detector(model, img_pth)
        bbox_result, segm_result = result
        bboxes = np.vstack(bbox_result)
        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)
            for i, bbox in enumerate(bbox_result)
        ]
        labels = np.concatenate(labels)

        gt_pairs = get_gt(annotations)
        img = cv2.imread(img_pth)

        result_pairs = []
        for bbox, label in zip(bboxes, labels):
            if label == 0:
                result_pairs.append((label, (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))))
                cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 255, 0))

        if show:
            print(img_pth)
            cv2.imshow("img", img)
            cv2.waitKey(0)

        to_compare = tester.connect_pairs(gt_pairs, result_pairs, dummy_pair=(1, (-1, -1, 0, 0)))
        compare(to_compare, final_results)

    for k, v in final_results.items():
        tester.print_results(k.capitalize(), v, task="detection")


def get_gt(annotations):
    """
    Get ground truth data for a specific file.

    :param annotations: A list of lists containing bboxes in coco format.
    :return: A list of tuples (label, [coordinates]).
    """
    gt_pairs = []
    for anno in annotations:
        x, y, w, h = anno
        coords = (x, y, x + w, y + h)
        gt_pairs.append((0, coords))

    return gt_pairs


def compare(pairs, result):
    """
    Compare ground truth and real data. Calculate metrics.

    :param pairs: A list of tuples representing potential ground truth<->real data pairs.
    :param result: A result dict.
    """
    from vision.helpers.box_helpers import bb_intersection_over_union
    for gt, rd in pairs:
        # this is very restrictive, if there is proper box, but with incorrect label it's fp and fn simultaneously
        keys = ["tp"] if gt[0] == rd[0] else ["fp"] if gt[0] == 0 else ["fn"] if rd[0] == 0 else ["fp", "fn"]
        for key in keys:
            result["meals"]["class"][key] += 1

        result["meals"]["boxes"].append(bb_intersection_over_union(gt[1], rd[1]))


if __name__ == '__main__':
    test(SRC_PATH, CFG_PATH, CKPT_PATH, show=False)
