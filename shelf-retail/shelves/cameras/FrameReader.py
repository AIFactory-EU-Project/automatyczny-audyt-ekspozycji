import logging
import time
import traceback
from datetime import datetime, timedelta
import os
import cv2
import numpy as np
import requests
import rtsp
from requests.auth import HTTPDigestAuth


class FrameReader:
    _REPEAT_INTERVALS = [1, 60, 300, 600]

    def __init__(self, camera_type, camera_ip, save_frame_dir, username='admin', password='Kamery2019!'):
        self.username = username
        self.password = password
        self.camera_ip = camera_ip
        self.save_frame_dir = save_frame_dir
        self.camera_type = camera_type

        # specify function for getting frames based on camera type
        if camera_type == 'dahua':
            self.get_frame_func = FrameReader.get_frame_dahua
        elif camera_type == 'hikvision':
            self.get_frame_func = FrameReader.get_frame_hikvision
        else:
            raise ValueError('Wrong camera type')

    def get_frame(self):
        """Get frame from camera using function specified in constructor

        :return (ndarray:BGR image, string:camera_type_camera_ip)
        """
        return self.get_frame_func(self), '{}_{}'.format(self.camera_type, self.camera_ip)

    def save_frames(self):
        """Save frame from camera every _REPEAT_INTERVAL seconds frames_num times"""
        for interval in self._REPEAT_INTERVALS:
            time.sleep(interval)
            real_time = datetime.now()
            timestamp = real_time.strftime("%d-%b-%Y_%H:%M:%S")
            photo_filename = '{}_{}_{}.png'.format(self.camera_type, self.camera_ip, timestamp)
            try:
                img, _ = self.get_frame()
                if img is not None:
                    photo_path = os.path.join(self.save_frame_dir, photo_filename)
                    r = cv2.imwrite(photo_path, img)
                    if r:
                        logging.info('Image saved: {}'.format(photo_path))
                    else:
                        logging.error('Cannot write frame: {}'.format(photo_path))
                else:
                    logging.error('Cannot get frame: {}'.format(photo_filename))
            except Exception as e:
                logging.error('Unexpected exception occured at {}'.format(photo_filename))
                logging.error(traceback.format_exc())

    def get_frame_dahua(self):
        # or auth=(self.username, self.password) if camera is in base auth mode
        try:
            r = requests.get('http://{}:80/cgi-bin/snapshot.cgi'.format(self.camera_ip),
                         auth=HTTPDigestAuth(self.username, self.password))
            return cv2.imdecode(np.frombuffer(r.content, dtype=np.uint8), -1)
        except requests.exceptions.ConnectionError as e:
            logging.error('ConnectionError at: {}: {}'.format(self.camera_ip, e))

    def get_frame_hikvision(self):
        url = 'rtsp://{}:{}@{}:554/Streaming/Channels/1'.format(self.username, self.password, self.camera_ip)
        try:
            with rtsp.Client(rtsp_server_uri=url) as client:
                img = client.read()
            # convert from PIL to np.array
            img = np.array(img)
            # Convert RGB to BGR
            return img[:, :, ::-1].copy()
        except cv2.error as e:
            logging.error('cv2.error at camera_ip: {}: {}'.format(self.camera_ip, e))
