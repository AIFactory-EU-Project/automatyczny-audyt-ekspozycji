"""
Config used for augmenting data
data_dir: input directory to augment
augment_dir: output directory where augmented data will be stored
yaml_filename: name of yaml file;
               if in another place than active file, pass 'dir' argument to TransformationManager, specifying where it can be found
divide_by_subdirs: if True and data to augment is splitted into three sets (train, test, val), each image from each set will land in respective augmented set
copy_original: if True, original, non-augmented data will be copied to augment dirs
ignore_json: if True, augment only images
mix_data: if True, data from different original sets will land in different augmented sets (antonym of divide_bu_subdirs)
augment_ratio: ratio of original images to augment
augment_repat: how many times each image will be augmented
train_ratio and val_ratio: ratio of images to land in train and val dirs (needed only when divide_by_subdirs in False)
"""


class Config:
    class Base:
        data_dir = "/tytan/raid/drugs-counter/datasets/tabcin_gripex/original"
        augment_dir = "/tytan/raid/drugs-counter/datasets/tabcin_gripex/augmented_test"
        yaml_filename = "config.yaml"
        layer_name = "layer1"
        divide_by_subdirs = True
        copy_original = True
        ignore_json = False
        mix_data = False     # use when images from one dataset should end in many augmented datasets
        augment_ratio = .6
        augment_repeat = 5
        train_ratio = .8
        val_ratio = .1
