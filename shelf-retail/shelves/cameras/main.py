import logging
from logger import configure_logging
import traceback
import json
import os
import threading
import time
import schedule
import sys
from shelves.cameras.FrameReader import FrameReader


configure_logging("/tmp/shelves-cameras-main.log")


def run_threaded(job_func, *args):
    job_thread = threading.Thread(target=job_func, args=args)
    job_thread.start()


def with_tb(outer):
    def inner(*args, **kwargs):
        try:
            return outer(*args, **kwargs)
        except:
            logging.error(traceback.format_exc())
    return inner


def main():
    run_at = None
    if len(sys.argv) == 2:
        run_at = sys.argv[1]
        logging.info("Will run at: {}".format(run_at))

    with open('config.json', 'r') as fp:
        config = json.load(fp)

    frame_readers = []
    for shop in config['shops'].items():
        if not os.path.exists(os.path.join(config["save_dir"], shop[1])):
            os.makedirs(os.path.join(config["save_dir"], shop[1]))
    for camera_info in config['cameras']:
        shop_name = config["shops"][camera_info['ip'][:-4]]
        reader = FrameReader(camera_type=camera_info['type'], camera_ip=camera_info['ip'],
                             save_frame_dir=os.path.join(config['save_dir'], shop_name), username=config['username'],
                             password=config['password'])
        if run_at == None:
            segment_hours = config['segments'][camera_info['segment']]
        else:
            segment_hours = [run_at]
        for hour in segment_hours:
            schedule.every().day.at(hour).do(run_threaded, with_tb(reader.save_frames))

        frame_readers.append(reader)

    logging.info('-----------------Jobs scheduled correctly-----------------')
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
