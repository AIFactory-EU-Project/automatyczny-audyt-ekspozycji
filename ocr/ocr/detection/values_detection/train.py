import os


def train():
    from tools.train import main as mmdetection_train
    mmdetection_train(["detector/gcnet.py", "--launcher", "pytorch", "--validate"])


if __name__ == '__main__':
    # set the device to run training on
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    # pytorch distributed training set up - needed for training with validation
    # if run multiple trainings, master port must be unique for each of them
    if 'RANK' not in os.environ:
        os.environ['RANK'] = str(0)
    if 'WORLD_SIZE' not in os.environ:
        os.environ['WORLD_SIZE'] = str(1)
    if 'MASTER_ADDR' not in os.environ:
        os.environ['MASTER_ADDR'] = '192.168.44.100'
    if 'MASTER_PORT' not in os.environ:
        os.environ['MASTER_PORT'] = str(8523)

    train()
