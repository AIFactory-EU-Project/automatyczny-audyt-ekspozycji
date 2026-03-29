import glob
import json
import os

import mmcv
import numpy as np
from mmcv.parallel import MMDataParallel
from mmcv.runner import load_checkpoint
from mmdet.apis import inference_detector, init_dist
from mmdet.models import build_detector

from vision.helpers.via_json_manipulation import rename_json_keys
from vision.tensorflow.detection.testing import detector_tester as tester

SRC_DIR = "/tytan/raid/shelf-retail/data/detection/grills_extracted/TEST"
CFG_PATH = "../../../models/detection/grills/cascade_mask_rcnn_r4_gcb_dconv_c3-c5_x101_32x4d_fpn_syncbn_1x.py"
CKPT_PATH = "/tytan/raid/shelf-retail/models/detection/grills_extracted/v1/cascade_mask_rcnn_r4_gcb_dconv_c3-c5_x101_32x4d_fpn_syncbn_1x/latest.pth"


def test(src_dir, cfg_path, ckpt_path):
    """6
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

    with open(os.path.join(src_dir, "via_region_data.json")) as f:
        json_data = json.load(f)
    rename_json_keys(json_data)

    final_results = {
        "grills": {
            "class": {"tp": 0, "fp": 0, "fn": 0},
            "boxes": []
        },
    }

    img_png = list(glob.iglob(src_dir + '**/*.png', recursive=True))
    img_jpg = list(glob.iglob(src_dir + '**/*.jpg', recursive=True))
    img_bmp = list(glob.iglob(src_dir + '**/*.bmp', recursive=True))

    img_pths = img_png+img_jpg+img_bmp

    for img_pth in img_pths:
        result = inference_detector(model, img_pth)
        bbox_result, segm_result = result
        bboxes = np.vstack(bbox_result)
        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)
            for i, bbox in enumerate(bbox_result)
        ]
        labels = np.concatenate(labels)

        gt_pairs = get_gt(json_data[os.path.basename(img_pth)])

        result_pairs = []
        for bbox, label in zip(bboxes, labels):
            # filter by accuracy
            if bbox[4] > 0.8 and (label == 0 or label == 1):
                result_pairs.append((label, (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))))

        to_compare = tester.connect_pairs(gt_pairs, result_pairs, dummy_pair=(2, (-1, -1, 0, 0)))
        compare(to_compare, final_results)

    for k, v in final_results.items():
        tester.print_results(k.capitalize(), v, task="detection")


def get_gt(file_data):
    """
    Get ground truth data for a specific file.

    :param file_data: A json data containing all annotations for a specific file.
    :return: A list of tuples (label, [coordinates]).
    """
    gt_pairs = []
    for key, region in file_data["regions"].items():
        x = region['shape_attributes']["x"]
        y = region['shape_attributes']["y"]
        w = region['shape_attributes']["width"]
        h = region['shape_attributes']["height"]
        coords = (x, y, x + w, y + h)
        label = int(region['region_attributes']["label"]) - 1
        gt_pairs.append((label, coords))

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
            result["grills"]["class"][key] += 1

        result["grills"]["boxes"].append(bb_intersection_over_union(gt[1], rd[1]))


if __name__ == '__main__':
    test(SRC_DIR, CFG_PATH, CKPT_PATH)
