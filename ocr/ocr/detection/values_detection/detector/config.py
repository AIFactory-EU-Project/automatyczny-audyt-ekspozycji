import random


class BaseConfig:
    # --- data
    data_path = "/tytan/raid/neuca/data/detection/values/balanced_legacy/"
    img_size = (800, 800)

    # -- training
    batch_size = 4
    epochs = 12
    iou_thresh = 0.8
    log_interval = 50
    learning_rate = 0.015
    momentum = 0.9
    weight_decay = 0.001
    # possible types: ['ASGD', 'Adadelta', 'Adagrad', 'Adam', 'Adamax', 'LBFGS', 'Optimizer', 'RMSprop', 'Rprop', 'SGD', 'SparseAdam']
    # warning! params for each type may differ
    optimizer = dict(type="SGD", lr=learning_rate, momentum=momentum, weight_decay=weight_decay)

    # learning rate policy
    lr_config = dict(
        policy='step',
        warmup='linear',
        warmup_iters=500,
        warmup_ratio=1.0 / 3,
        step=[8, 11],
        by_epoch=False)

    # --- evaluation
    # frequency of saving checkpoints in terms of iterations
    eval_interval = 100
    # save n-best checkpoints (basing on fscore)
    n_best = 3


class GCNetConfig(BaseConfig):
    # --- model
    # backbone is one of ResNet-50 or ResNet-101
    backbone_depth = 101

    # --- training
    work_dir = "/tytan/raid/neuca/models/detection/values/legacy/balanced/gcnet/v1"


class GCNetSearch(GCNetConfig):
    # --- model
    if random.getrandbits(1):
        backbone_depth = 50
        batch_size = 6

    # --- training
    work_dir = "/tytan/raid/neuca/models/detection/values/legacy/balanced/gcnet/v1-search/4"
    learning_rate = random.uniform(0.0001, 0.01)
    weight_decay = random.uniform(0.0001, 0.1)
    momentum = random.uniform(0, 0.9)
    sgd_optimizer = dict(type="SGD", lr=learning_rate, momentum=momentum, weight_decay=weight_decay)
    adam_optimizer = dict(type="Adam", lr=learning_rate, weight_decay=weight_decay)
    optimizer = random.choice([sgd_optimizer, adam_optimizer])


class CascadeRCNNConfig(BaseConfig):
    work_dir = "/tytan/raid/neuca/models/detection/values/legacy/balanced/cascade/v1"
