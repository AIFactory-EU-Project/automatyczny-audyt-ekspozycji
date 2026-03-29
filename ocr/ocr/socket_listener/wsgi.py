import atexit

from vision.deploy import sockets

from ocr.socket_listener.box_analyser_worker_service import create_box_service

service = create_box_service()
atexit.register(service.shutdown)


def handle_request(environ, _):
    return sockets.handle_request(service, environ)
