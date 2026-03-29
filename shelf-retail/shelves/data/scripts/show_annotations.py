import glob
import json
import cv2

SRC_DIR = "/tytan/raid/shelf-retail/data/orig/detection/meals"


def show(src_dir):
    for json_pth in glob.iglob(src_dir + "/**/*.json", recursive=True):
        if "classes.json" in json_pth:
            continue

        with open(json_pth, "r") as f:
            json_data = json.load(f)

        for entry in json_data:
            img = cv2.imread(entry["localPath"])
            for region in entry["regions"]:
                x = region["x"]
                y = region["y"]
                w = region["width"]
                h = region["height"]
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)

            print(entry["localPath"])
            cv2.imshow("Image with anno", img)
            cv2.waitKey(0)


if __name__ == '__main__':
    show(SRC_DIR)
