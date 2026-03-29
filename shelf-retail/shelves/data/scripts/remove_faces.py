"""Remove faces from the photo"""

import numpy as np
import cv2
import face_alignment


def detect_faces(img):
    """
    Detect faces on the given image.

    :param img: An image to detect on.
    :return: A list of detected faces' bounding boxes.
    """
    fd = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D).face_detector
    face_bboxes = fd.detect_from_image(img)
    return [bbox.astype(np.int).tolist()[:4] for bbox in face_bboxes]


def remove_faces(img_pth):
    """
    Remove faces from the given image.

    :param img_pth: A path to the image.
    """
    img = cv2.imread(img_pth)
    face_bboxes = detect_faces(img)
    for bbox in face_bboxes:
        x1, y1, x2, y2 = bbox
        box = img[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2), :]
        box[:] = cv2.GaussianBlur(box, (25, 25), 5)
    cv2.imshow("Blurred faces", img)
    cv2.waitKey()


if __name__ == '__main__':
    remove_faces("/home/natalia/dahua_172.16.12.251_16-Oct-2019_19:00:01.png")
