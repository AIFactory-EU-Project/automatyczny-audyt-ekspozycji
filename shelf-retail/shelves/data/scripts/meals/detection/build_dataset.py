from shelves.data.scripts.convert_to_coco import read_data, save_subset_in_coco_format

SRC_DIR = "/tytan/raid/shelf-retail/data/orig/detection/meals"
DST_DIR = "/tytan/raid/shelf-retail/data/detection/meals/v02"
SPLIT = {
    "val": ["7", "10", "12", "15"]
}


def split_into_subsets(data, split):
    train = []
    val = []
    for d in data:
        set_number = d["filename"].split(".")[2]
        if set_number in split["val"]:
            val.append(d)
        else:
            train.append(d)

    return train, val, []


def convert_to_coco(src_dir, dst_dir, split=SPLIT):
    data = read_data(src_dir)
    train_subset, validation_subset, test_subset = split_into_subsets(data, split)

    save_subset_in_coco_format(train_subset, dst_dir, src_dir, split_name='train')
    save_subset_in_coco_format(validation_subset, dst_dir, src_dir, split_name='validation')
    save_subset_in_coco_format(test_subset, dst_dir, src_dir, split_name='test')


if __name__ == '__main__':
    convert_to_coco(SRC_DIR, DST_DIR, SPLIT)
