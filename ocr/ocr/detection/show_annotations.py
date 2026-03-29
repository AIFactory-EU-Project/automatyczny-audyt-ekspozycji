import json
import os
import cv2


SRC_PTH = "/tytan/raid/neuca/data/detection/values/aug13/annotations/train.json"


def show(src_pth):
    with open(src_pth, "r") as f:
        json_data = json.load(f)

    start = 0
    for img_data in json_data["images"]:
        img_pth = os.path.join(os.path.dirname(os.path.dirname(src_pth)), os.path.basename(src_pth).split(".")[0], img_data["file_name"])
        img = cv2.imread(img_pth)
        for anno_data in json_data["annotations"][start:]:
            if anno_data["image_id"] != img_data["id"]:
                break
            bbox = [int(e) for e in anno_data["bbox"]]
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (0, 255, 255))
            start += 1

        print(img_pth)
        cv2.imshow("Image with anno", img)
        cv2.waitKey(0)


if __name__ == '__main__':
    show(SRC_PTH)
