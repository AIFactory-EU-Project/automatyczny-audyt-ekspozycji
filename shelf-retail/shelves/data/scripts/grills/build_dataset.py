from shelves.data.scripts.convert_to_coco import convert_to_coco

SRC_DIR = "/tytan/raid/shelf-retail/data/orig/detection/grills_extracted"
DST_DIR = "/tytan/raid/shelf-retail/data/detection/grills_extracted/v02"
SPLIT = {
    "train": .8,
    "validation": .2,
    "test": .0
}

if __name__ == '__main__':
    convert_to_coco(SRC_DIR, DST_DIR, SPLIT)
