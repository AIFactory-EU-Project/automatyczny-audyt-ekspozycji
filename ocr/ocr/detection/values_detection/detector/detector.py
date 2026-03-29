import os
import mmcv
import numpy as np

from mmcv.parallel import MMDataParallel
from mmcv.runner import load_checkpoint, init_dist
from mmdet.apis import inference_detector
from mmdet.models import build_detector


class GCNetDetector:
    def __init__(self, ckpt_path, cfg_path="detector/gcnet.py", detection_threshold=.1):
        self.cfg_path = cfg_path
        self.ckpt_path = ckpt_path
        self.detection_threshold = detection_threshold
        self.model = self.init_model()

    def init_model(self):
        if 'RANK' not in os.environ:
            os.environ['RANK'] = str(0)
        if 'WORLD_SIZE' not in os.environ:
            os.environ['WORLD_SIZE'] = str(1)
        if 'MASTER_ADDR' not in os.environ:
            os.environ['MASTER_ADDR'] = '192.168.44.100'
        if 'MASTER_PORT' not in os.environ:
            os.environ['MASTER_PORT'] = str(8522)

        cfg = mmcv.Config.fromfile(self.cfg_path)
        model = build_detector(
            cfg.model, train_cfg=None, test_cfg=cfg.test_cfg)
        load_checkpoint(model, self.ckpt_path)
        init_dist("pytorch", **cfg.dist_params)

        model = MMDataParallel(model, device_ids=[0])
        model.cfg = cfg
        return model

    def predict(self, img_path):
        def process_result(result):
            bbox_result, segm_result = result
            bboxes = np.vstack(bbox_result)
            labels = [
                np.full(bbox.shape[0], i, dtype=np.int32)
                for i, bbox in enumerate(bbox_result)
            ]
            labels = np.concatenate(labels)
            return bboxes, labels

        if isinstance(img_path, list):
            results = []
            for img_p in img_path:
                result = inference_detector(self.model, img_p)
                results.append(process_result(result))
            return results

        else:
            result = inference_detector(self.model, img_path)
            return process_result(result)
