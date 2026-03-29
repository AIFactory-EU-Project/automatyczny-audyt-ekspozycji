#!/bin/bash
# ping all routers
# usage: ./ping-routers.sh | grep '100%' -B1
for i in {1..20}
do
    ping -c 1 -W 5 172.16.$i.1
done
