#!/bin/bash

mdadm --stop /dev/md8
mdadm --create /dev/md8 --name tytan-storage --raid-devices=6 --level=5 --assume-clean /dev/sdj /dev/sde /dev/sdi /dev/sdh /dev/sdg /dev/sdf
mount /tytan/storage

