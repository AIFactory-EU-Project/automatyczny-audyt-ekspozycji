from multiprocessing import Queue

from vision.deploy.processes import WorkerProcess


class WorkerService:

    def __init__(self, worker, configs):
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.detection_process = WorkerProcess(self.input_queue, self.output_queue, worker, configs)
        self.detection_process.start()

    def process(self, image_paths):
        self.input_queue.put(image_paths)
        return self.output_queue.get()

    def shutdown(self):
        self.detection_process.shutdown()
        self.detection_process.join()
