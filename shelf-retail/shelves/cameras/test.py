import cv2
import sys

from shelves.cameras.FrameReader import FrameReader

USERNAME = 'admin'
PASSWORD = '111222qqqwww'
DESTDIR="/home/staszek/tmp/photos/"

def test():
    print("I init reader 1")
    reader = FrameReader(camera_type='dahua', camera_ip='172.16.1.252',
        save_frame_dir=None, username=USERNAME, password=PASSWORD)
    print("I get frame 1")
    img, _ = reader.get_frame()
    print("I write frame 1")
    cv2.imwrite(DESTDIR + "test1.jpg", img)
    # cv2.imshow('win', img)
    # cv2.waitKey(0)

    print("I init reader 2")
    reader = FrameReader(camera_type='hikvision', camera_ip='172.16.3.253',
        save_frame_dir=None, username=USERNAME, password=PASSWORD)
    print("I get frame 2")
    img, _ = reader.get_frame()
    print("I write frame 2")
    cv2.imwrite(DESTDIR + "test2.jpg", img)
    # cv2.imshow('win', img)
    # cv2.waitKey(0)

if __name__ == "__main__":
    test()
