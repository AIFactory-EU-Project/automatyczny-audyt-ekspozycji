#!/usr/bin/env python3
""" Script to download camera frames en masse
"""
import json
import os
import sys
import time
from camera_service.frame_reader import get_frame, Error

blacklist = [
    # due to being offline
    '172.16.3.252',
    '172.16.3.253',
    '172.16.3.251',
    
    '172.16.4.252',
    '172.16.4.253',
    '172.16.4.251',
    
    '172.16.14.252',
    '172.16.14.253',
    '172.16.14.251',
        
    '172.16.15.252',
    '172.16.15.253',
    '172.16.15.251',
    
    '172.16.18.252',
    '172.16.18.253',
    '172.16.18.251',
    
]

# set download_dir with command line argument
download_dir=sys.argv[1] if len(sys.argv)==2 else None

# read config
loc=os.path.dirname(__file__)
with open(os.path.join(loc, 'config.json')) as f:
    cfg = json.load(f)

# download frame from each camera
for c in cfg['cameras']:
    print(c['ip'], c['type'])
    if c['ip'] in blacklist:
        print('skipping')
    else:        
        try:
            t0=time.time()
            img = get_frame(c['ip'], c['type'], cfg['username'], cfg['password'])
            t1=time.time()
            print(f"download_time_sec {(t1-t0):.3f}")
        except Error as e:
            print(e)
        # save image
        if download_dir is not None:
            with open(os.path.join(download_dir,'{}_{}.png'.format(c['ip'], c['type'])), 'wb') as f:
                f.write(img)


