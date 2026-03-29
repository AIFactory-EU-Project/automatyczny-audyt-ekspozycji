import os
from pprint import pprint

import numpy as np
from keras.callbacks import Callback

from vision.monitor import monitor


class MonitorCallback(Callback):

    def __init__(self, name):
        super(MonitorCallback).__init__()
        self.losses = []
        self.epoch = 0
        self.monitor_group = name
        self.monitor_time = "6h"

    def on_epoch_end(self, epoch, logs=None):
        self.epoch += 1
        self.losses = []

        monitor.monitor(self.monitor_group, "epochs", self.epoch, time=self.monitor_time)
        monitor.monitor_float(self.monitor_group, "loss", logs['loss'], time=self.monitor_time)
        monitor.monitor_float(self.monitor_group, "val_loss", logs['val_loss'], time=self.monitor_time)

    def on_batch_end(self, batch, logs=None):
        self.losses.append(logs["loss"])
        loss = np.mean(self.losses)

        monitor.monitor_float(self.monitor_group, "batch_loss", logs["loss"], time=self.monitor_time)
        monitor.monitor_float(self.monitor_group, "loss", loss, time=self.monitor_time)

    def on_train_begin(self, logs=None):
        monitor.starting(self.monitor_group, "epochs", time=self.monitor_time)
        monitor.starting(self.monitor_group, "batch_loss", time=self.monitor_time)
        monitor.starting(self.monitor_group, "loss", time=self.monitor_time)
        monitor.starting(self.monitor_group, "val_loss", time=self.monitor_time)


class TestEvaluator(Callback):

    def __init__(self, generators, metrics, labels, cm_tb_callback_cm=None, cm_save_dir=None, postprocess=None):
        """
        Callback for evaluating models on additional test generators. Metrics are evaluated on entire test sets,
        which enables correct computation of per-class metrics (like F1 score).

        :param generators: dataset generators
        :param metrics: metrics to be evaluated, can be implemented in numpy
        :param labels: class names
        :param cm_tb_callback_cm: tensorboard callback - pass it show confusion matrices in TensorBoard
        :param cm_save_dir: save directory for confusion matrices, if CM are to be generated
        """
        super(TestEvaluator, self).__init__()
        if isinstance(generators, list):
            self.generators = generators
        else:
            self.generators = [generators]
        self.metrics = metrics
        self.metrics_names = [m.__name__ for m in metrics]
        self.labels = labels

        self.cm_tb_callback = cm_tb_callback_cm
        self.cm_save_dir = cm_save_dir

        self.postprocess = postprocess or {"":None}

    def on_epoch_end(self, epoch, logs=None):
        if not self.generators:
            return {}

        metrics = []
        metrics_names = []
        for i, generator in enumerate(self.generators):
            if generator is None:
                continue

            # Prepare test set name suffix
            suffix = ''
            prefix = ''
            if len(self.generators) > 1:
                suffix += str(i+1)
                if hasattr(generator, 'name') and generator.name:
                    suffix += '_' + generator.name
                    prefix += generator.name + '_'

            print('Evaluating on test{} set...'.format(suffix))

            # Collect outputs
            ys_orig = []
            gts_orig = []
            for k in range(len(generator)):
                x, gt = generator[k]
                gts_orig.append(gt)
                ys_orig.append(self.model.predict(x))

            for postprocess_name, postprocess in self.postprocess.items():

                ys = [list(map(postprocess,v)) for v in ys_orig] if postprocess else ys_orig
                gts = [list(map(postprocess,v)) for v in gts_orig] if postprocess else gts_orig

                ys = np.concatenate(ys, axis=0)
                gts = np.concatenate(gts, axis=0)

                suffix2 = "_" + postprocess_name if postprocess_name else ""

                # Calculate metrics
                this_metrics = []
                this_metrics_names = []
                for metric, metric_name in zip(self.metrics, self.metrics_names):
                    value = metric(prediction=ys, gt=gts)
                    name = 'test' + suffix + suffix2 + '_' + metric_name
                    if np.isscalar(value):
                        this_metrics.append(value)
                        this_metrics_names.append(name)
                    else:
                        for i, v in enumerate(value):
                            n = "{name}_{i:02}".format(**locals())
                            this_metrics.append(v)
                            this_metrics_names.append(n)

                metrics.append(this_metrics)
                metrics_names.append(this_metrics_names)

                # Plot confusion matrix
                if self.cm_tb_callback or self.cm_save_dir:
                    from vision.metrics.numpy.multiclass import plot_confusion_matrix
                    fig = plot_confusion_matrix(gts, ys, self.labels)

                    if self.cm_save_dir:
                        figname = "{epoch:04d}{prefix}{suffix2}.png".format(**locals())
                        os.makedirs(self.cm_save_dir, exist_ok=True)
                        fig.savefig(os.path.join(self.cm_save_dir, figname))

                    if self.cm_tb_callback:
                        summary = self._figure_to_summary(fig, tag='cm'+suffix+suffix2)
                        self.cm_tb_callback.writer.add_summary(summary, epoch)

        # Calculate mean metrics for all test sets
        if len(self.generators) > 1 and len(metrics):
            mean_metrics = np.mean(metrics, axis=0)
            metrics.append(mean_metrics)
            metrics_names.append(['test_' + m for m in self.model.metrics_names])

        # Prepare the result
        results = {}
        for names, m in zip(metrics_names, metrics):
            results.update(dict(zip(names, m)))

        if results:
            pprint(results)

        # Update logs
        logs.update(results)

        return results

    def _figure_to_summary(self, fig, tag):
        """
        Source: https://stackoverflow.com/questions/41617463/tensorflow-confusion-matrix-in-tensorboard

        Converts a matplotlib figure ``fig`` into a TensorFlow Summary object
        that can be directly fed into ``Summary.FileWriter``.
        :param fig: A ``matplotlib.figure.Figure`` object.
        :return: A TensorFlow ``Summary`` protobuf object containing the plot image
                 as a image summary.
        """
        import io
        import tensorflow as tf

        w, h = fig.canvas.get_width_height()

        # get PNG data from the figure
        png_buffer = io.BytesIO()
        fig.canvas.print_png(png_buffer)
        png_encoded = png_buffer.getvalue()
        png_buffer.close()

        summary_image = tf.Summary.Image(height=h, width=w, colorspace=4,  # RGB-A
                                         encoded_image_string=png_encoded)
        summary = tf.Summary(value=[tf.Summary.Value(tag=tag, image=summary_image)])
        return summary


class LRLogger(Callback):
    def on_epoch_end(self, epoch, logs=None):
        from keras import backend as K
        logs["LR"] = K.eval(self.model.optimizer.lr)
