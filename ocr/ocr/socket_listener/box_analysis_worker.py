import time

from vision.deploy.workers import Worker

from ocr.scanner.aocr import Ocr
from ocr.scanner.barcodes import BarcodeReader
from ocr.scanner.boxes import BoxProcessor
from ocr.scanner.detector import Detector
from ocr.scanner.parser import TextParser
from ocr.scanner.worker import Queue


class BoxAnalysisWorker(Worker):

    def __init__(self):
        self.boxes = Queue()
        self.parser = TextParser(self.boxes)
        self.ocr = Ocr(self.parser.inputs)
        time.sleep(3)
        self.detector = Detector(self.ocr.inputs)
        self.barcode_reader = BarcodeReader(self.detector.inputs)
        self.box_processor = BoxProcessor(self.barcode_reader.inputs)

    def process(self, image_paths):
        self.box_processor.inputs.put(image_paths)
        box = self.boxes.get()
        return box
