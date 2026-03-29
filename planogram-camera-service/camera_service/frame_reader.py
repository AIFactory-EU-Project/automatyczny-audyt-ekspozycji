import logging
import cv2
import numpy as np
import requests
import time
from requests.auth import HTTPDigestAuth, HTTPBasicAuth


class Error(Exception):
    def __init__(self, status, description=""):
        self.status=status
        self.description=description
    def __str__(self):
        return "{}: {}: {}".format(self.__class__.__name__, self.status, self.description)


def get_frame_dahua(cam_ip:str, usr:str, pwd:str):
    """ Get image frame from dahua camera
    :param cam_ip: camera IP
    :param usr: username
    :param pwd: password
    :return: image as BGR numpy array
    """
    # or auth=(self.username, self.password) if camera is in base auth mode
    # ^and when is that?
    try:
        r = requests.get(url='http://{}:80/cgi-bin/snapshot.cgi'.format(cam_ip),
            auth=HTTPDigestAuth(usr, pwd),
            #auth=HTTPBasicAuth(usr, pwd),
            timeout=60)
        if r.status_code==200:
            return cv2.imdecode(np.frombuffer(r.content, dtype=np.uint8), -1)
        elif r.status_code==401:
            raise Error(401)
        else:
            e = Error(r.status_code, "unexpected error from dahua")
            logging.info(e)
            raise e
    except requests.exceptions.ConnectionError as e:
        e = Error(504, "cannot connect to camera dahua {}".format(cam_ip))
        logging.info(e)
        raise e


def get_frame_hikvision(cam_ip:str, usr:str, pwd:str):
    """ Get image frame from hikvision camera
    :param cam_ip: camera IP
    :param usr: username
    :param pwd: password
    :return: image as BGR numpy array
    """
    url = 'rtsp://{}:{}@{}:554/Streaming/Channels/1'.format(usr, pwd, cam_ip)
    try:
        stream=cv2.VideoCapture(url)
        if stream is not None and stream.isOpened():
            time.sleep(.5)
            grabbed, frame = stream.read()
            if not grabbed:
                e = Error(504, "no frame available")
                logging.info(e)
                raise e
            return frame
        else:
            e = Error(504, "cannot open rstp stream")
            logging.info(e)
            raise e

    finally:
        if stream:
            stream.release()


def get_frame(cam_ip:str, cam_type:str, usr:str, pwd:str)->bytes:
    """ Get png encoded frame from camera
    :param cam_ip: camera IP address
    :param cam_type: camera type 'dahua' or 'hikvision'
    :param usr: username
    :param pwd: password
    :return: png encoded image
    """
    if cam_type == 'dahua':
        img=get_frame_dahua(cam_ip, usr, pwd)
    elif cam_type == 'hikvision':
        img=get_frame_hikvision(cam_ip, usr, pwd)
    else:
        e = Error(400, 'Wrong camera type')
        logging.info(e)
        raise e
    retval, buf = cv2.imencode(".png", img)
    if not retval:
        e = Error(500, 'imencode retval={}'.format(retval))
        logging.error(e)
        raise e
    return buf.tobytes()

