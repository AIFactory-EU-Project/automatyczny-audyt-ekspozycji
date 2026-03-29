import cv2
from manager import TransformationManager


def transform_lena():
    lena = cv2.imread('lena.jpg')
    manager = TransformationManager('template.yaml')
    lena = manager.apply_transformations(lena, 'layer1')
    cv2.imshow('lena', lena)
    cv2.waitKey()


if __name__ == "__main__":
    for _ in range(0, 10):
        transform_lena()
