import logging
import os
import numpy as np
import mmcv

import torch
from mmdet.apis import inference_detector, init_detector
import mmcv

CFG_PTH = os.path.join(os.path.dirname(__file__), "../../models/configs/grills_cfg.py")
CKPT_PTH = os.path.join(os.path.dirname(__file__), "../../models/bin/grills.pth")


_grill_model = None


def get_grill_model():
    global _grill_model

    if _grill_model is None:
        logging.info("load_grill_model")
        if not torch.distributed.is_initialized():
            torch.distributed.init_process_group(
                'NCCL', 
                init_method='file:///tmp/8cje872r', 
                rank=0, 
                world_size=1)

        model = init_detector(CFG_PTH, CKPT_PTH, device='cuda:0')
        _grill_model = model

    return _grill_model


def grill_report(img):
    model = get_grill_model()
    result = inference_detector(model, img)
    bbox_result, segm_result = result
    bboxes = np.vstack(bbox_result)
    labels = [
        np.full(bbox.shape[0], i, dtype=np.int32)
        for i, bbox in enumerate(bbox_result)
    ]
    labels = np.concatenate(labels)

    count = 0
    for bbox, label in zip(bboxes, labels):
        # filter by accuracy
        if bbox[4] > 0.8 and label == 1:
            count += 1

    return count



if __name__ == '__main__':
    #import cv2
    #os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    
    import imageio
    img = imageio.imread("/home/appuser/repos/planogram-ai-service/test/data/7.251.jpg")

    grill_report(img)
