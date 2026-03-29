import logging
import os
import numpy as np
import torch
import copy
from mmdet.apis import inference_detector, init_detector

from ai_service.ai.scripts.meals.classifier import get_classifier_model, preprocess_image
from ai_service.ai.scripts.meals.mappings.classifier_mapping import class_to_sku
from ai_service.ai.scripts.meals.mappings.sku_mapping import sku_mapping, sku_is_specific
from ai_service.ai.scripts.meals.shelves.shelves import planogram_boxes

CFG_PTH = os.path.join(os.path.dirname(__file__), "../../models/configs/meals_cfg.py")
CKPT_PTH = os.path.join(os.path.dirname(__file__), "../../models/bin/meals.pth")


_meals_detector = None


def get_meals_detector():
    global _meals_detector
    if _meals_detector is None:
        logging.info("load_meals_model")
        if not torch.distributed.is_initialized():
            torch.distributed.init_process_group(
                'NCCL', 
                init_method='file:///tmp/8cje872r', 
                rank=0, 
                world_size=1)

        model = init_detector(CFG_PTH, CKPT_PTH, device='cuda:0')
        _meals_detector = model
    return _meals_detector


def planogram_report(img, camera_ip):
    model = get_meals_detector()
    result = inference_detector(model, img)
    bbox_result, segm_result = result
    bboxes = np.vstack(bbox_result)
    labels = [
        np.full(bbox.shape[0], i, dtype=np.int32)
        for i, bbox in enumerate(bbox_result)
    ]
    labels = np.concatenate(labels)

    classifier = get_classifier_model("nasnet", 196, memory_fraction=0.2)

    boxes = []
    for bbox, label in zip(bboxes, labels):
        if bbox[4] > .3 and label == 0:
            x, y, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            roi = img[y:y2, x:x2]
            img_c = preprocess_image(roi)
            predictions = classifier.predict(np.array([img_c]))[0]

            pred = np.array(predictions >= .5, dtype=np.float32())
            positives = np.count_nonzero(pred == 1)
            if (pred == 0).all() or (positives == 1 and pred[-1] == 1):
                np.put(pred, 0, 1)
            
            classes = []
            for idx in np.where(pred == 1)[0]:
                sku_name = class_to_sku.get(idx, "Unknown")
                sku_idx = sku_mapping.get(sku_name, '0')
                classes.append((sku_idx, sku_name, predictions[idx]))

            # classes: [(sku_idx, sku_name, score)]
            if len(classes) > 1:
                # find best specific class
                best_row = ()
                best_score = 0.0
                for idx, name, score in classes:
                    # take class which has best score and is not general or Unknown class
                    if sku_is_specific(idx) and score > best_score:
                        best_score = score
                        best_row = (idx, name, score)
                # if there were no specific class, return the best general class
                if not best_row:
                    best_row = sorted(classes, key=lambda c: c[2])[0]
                classes = [best_row]

            sku_idx, sku_name, score = classes[0]
            box = {"topLeftX": x, "topLeftY": y, "width": x2-x, "height": y2-y,
                   "accuracy": int(bbox[4]*100), "skuIndex": sku_idx}
            boxes.append(box)

    return planogram_boxes(boxes, camera_ip)


if __name__ == '__main__':
    import cv2
    import json
    import sys
    if len(sys.argv)<=2:
        print('Usage: python3 planogram_report.py <path/to/image> <camera-ip>')
        sys.exit(1)
    path, camera_ip = sys.argv[1:3] 
    #try: /home/appuser/logs/175627bf-4734-46b8-aa41-6d9f54525c8e.png 172.16.1.252
    img = cv2.imread(path)    
    print(json.dumps(planogram_report(img, camera_ip)))

