from vision.config.auto import *
from vision.keras.train.batches import ClassifierBatchGenerator


@auto_config
class config(config):

    class base:
        # name of the model available in models.py file
        model_name = "mobilenet"
        # keras verbose level
        verbose_level = 1
        # how many gpus use to train
        gpus = 1
        # input size
        input = (224, 224, 3)
        # how many or how percent of first layers set to not train
        lock_first_layers = 0.0

    class sample_config(base):
        # directory name
        out_name = "sample"
        # where to put logs
        logging_path = "/path/to/trainings/{}".format(out_name)
        # where to put saved checkpoint
        checkpoint_path = "/path/to/trainings/{}".format(out_name)
        # how often validate the network (in epochs)
        checkpoint_interval = 1

        # additional metrics to observe (can be custom from metrics.py)
        metrics = ["binary_accuracy"]
        # what to monitor during validation
        monitoring_measure = "val_loss"
        # loss (can be custom from losses.py)
        loss_func = "categorical_crossentropy"
        # last activation type
        last_activation = "softmax"
        # keras optimizer
        optimizer = "nadam"
        # max number of epochs
        epochs = 100

        # additional params to generators (pad_image - don't wrap image, add border, grayscale - get rid of colors)
        generator_params = {"pad_image": True}
        # training generator
        generator = ClassifierBatchGenerator
        # validation generator
        val_generator = ClassifierBatchGenerator

        # path to training labels.txt
        data_path = "/path/to/train/labels.txt"
        # number of outputs
        number_of_class = 10
        # batch size
        train_batch_size = 128
        # number of batches in one epoch
        steps_per_epoch = sum(1 for _ in open(data_path)) // train_batch_size

        # whether validate network
        use_validation = True
        # path to validation labels.txt
        val_data_path = "/path/to/val/labels.txt"
        # validation batch size
        val_batch_size = 128
        # number of batches in validation epoch
        validation_steps = sum(1 for _ in open(val_data_path)) // val_batch_size

        # min delta in early stopping
        early_stopping_min_delta = 1e-6
        # how many epochs wait to decrease monitoring measure
        early_stopping_patience = 100
