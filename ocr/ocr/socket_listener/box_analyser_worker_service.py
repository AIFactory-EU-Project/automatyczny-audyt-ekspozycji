from vision.deploy.services import WorkerService

from webapi.common.service.deploy_config import default_pylons_detector_config, default_pylons_d_dd_ocr_config, \
    default_pylons_dd_dd_ocr_config, default_pylons_ddd_d_ocr_config
from webapi.common.service.workers import PylonWorker


class BoxAnalyserWorkerService(WorkerService):

    def __init__(self, detector_config, ocr_config):
        super().__init__(PylonWorker, [detector_config, ocr_config])

    def process(self, image_paths):
        result = super().process(image_paths)
        response = []
        for path, r in zip(image_paths, result):
            response.append({
                "image_path": path,
                "displays": [{
                    "box": box,
                    "detection_score": d_score,
                    "value": value,
                    "reading_score": r_score
                } for box, d_score, value, r_score in r["displays"]]
            })
        return response


def create_box_service():
    return BoxAnalyserWorkerService(default_pylons_detector_config, default_pylons_d_dd_ocr_config)

