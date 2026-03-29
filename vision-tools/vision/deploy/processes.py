import queue
import time
from multiprocessing import Process, Event

import cv2

from vision.tensorflow.gpus import tensorflow_use_gpus


class WorkerProcess(Process):

    def __init__(self, input_q, output_q, worker, configs):
        super(WorkerProcess, self).__init__()
        self.input_queue = input_q
        self.output_queue = output_q
        self.configs = configs
        self.worker = worker
        self.exit = Event()

    def run(self):
        nets_fraction = 0
        for c in self.configs:
            if hasattr(c, "gpu_memory_fraction") and c is not None:
                nets_fraction += c.gpu_memory_fraction
            else:
                nets_fraction += 1.0

        memory_fraction = min(1.0, nets_fraction)
        tensorflow_use_gpus(1, memory_limit_fraction=memory_fraction)

        worker = self.worker.from_config(*self.configs)

        while not self.exit.is_set():
            try:
                image_paths = self.input_queue.get_nowait()
                images = [cv2.imread(path) for path in image_paths]
                images = [img for img in images if img is not None]
                response = worker.process(images)
                self.output_queue.put(response)
            except queue.Empty:
                # don't saturate cpu
                time.sleep(0.01)

    def shutdown(self):
        self.exit.set()

