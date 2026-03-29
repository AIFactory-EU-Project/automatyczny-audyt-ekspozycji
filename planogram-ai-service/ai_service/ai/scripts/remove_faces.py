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
    # return only bboxes with score higher than .9
    return [bbox.astype(np.int).tolist()[:4] for bbox in face_bboxes if bbox[4:][0] > .9]


def remove_faces(img, percent=.15):
    """
    Remove faces from the given image.

    :param img: An image.
    :param percent: A percent to widen roi.
    :return: cv2 image
    """
    face_bboxes = detect_faces(img)
    im_height, im_width = img.shape[:2]
    for bbox in face_bboxes:
        x1, y1, x2, y2 = bbox
        # extend bounding box in every direction by the given percent
        roi_w, roi_h = int(percent*(x2-x1)), int(percent*(y2-y1))
        x1, y1 = x1-roi_w, y1-roi_h
        x2, y2 = x2+roi_w, y2+roi_h

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(im_width, x2)
        y2 = min(im_height, y2)

        box = img[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2), :]
        box[:] = (0, 0, 0)

    return img


if __name__ == '__main__':
    img = cv2.imread("/tytan/raid/shelf-retail/data/orig/detection/grills/2/dahua_172.16.12.251_16-Oct-2019_19:00:01.png")
    img = remove_faces(img)
    cv2.imshow("Removed faces", img)
    cv2.waitKey()
