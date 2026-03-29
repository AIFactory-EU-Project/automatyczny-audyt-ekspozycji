# create lmdb
import os

CAFFE_FORK_DIR = "/home/tytan/caffe-ssd/"

PYTHON_PATH = "PYTHONPATH=" + CAFFE_FORK_DIR + "python "

REDO = True
DATA_ROOT_DIR = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/"
DATASET_NAME = "DEEPFASHION"
LIST_DIR = "/tytan/raid/fashion/detection/lmdb/deepfashion/"
MAPFILE= "/tytan/raid/fashion/detection/lmdb/deepfashion/category_label.prototxt"
ANNO_TYPE = "detection"
DB = "lmdb"
MIN_DIM = 0
MAX_DIM = 0
WIDTH = 0
HEIGHT = 0

EXTRA_CMD = "--encode-type=jpg --encoded"
if REDO:
    EXTRA_CMD += " --redo"

for subset in ['trainval', 'test']:
    command_py = "python {0}/scripts/create_annoset.py --anno-type={1} --label-map-file={2} --min-dim={3} --max-dim={4} " \
                 "--resize-width={5} --resize-height={6} --check-label --shuffle {7} {8} {9}{10}.txt {9}{10}_{11} /tmp/tmpdb"\
        .format(CAFFE_FORK_DIR, ANNO_TYPE, MAPFILE, MIN_DIM, MAX_DIM, WIDTH, HEIGHT, EXTRA_CMD, DATA_ROOT_DIR, LIST_DIR, subset, DB)

    os.system(PYTHON_PATH + command_py)

command_img = "{0}build/tools/get_image_size {1} {2}test.txt {2}test_name_size.txt".format(CAFFE_FORK_DIR, DATA_ROOT_DIR, LIST_DIR)
os.system(command_img)
