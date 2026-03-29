class classifier:
    """
     augment_repeat - How many times an augmentation for a single image should be repeated
     val_to_train_ratio - How many validation images should there be per one train image
     aug_path - Destination path for augmentations
     data_path - Source path for data
     """
    augment_repeat = 1000
    val_to_train_ratio = 0.1
    aug_path = "/tytan/raid/shelf-retail/data/classification/aug/v02"
    data_path = "/tytan/raid/shelf-retail/data/orig/classification/december_skus"
