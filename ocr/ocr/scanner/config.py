class Scanner:
    logging = True
    visualize = False
    num_of_windows = 1

    class CameraLeft:
        images_pth = "/tytan/raid/tmp/natalia/neuca/testowe2/rekimarin_cam2"

    class CameraFront:
        images_pth = "/tytan/raid/tmp/natalia/neuca/testowe2/rekimarin_cam1"

    cameras = {
        "front": CameraFront,
        "left": CameraLeft
    }
