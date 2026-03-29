#!/bin/bash

if [[ "$1" =~ ^(-h|--help)$ ]]
then
    echo "Usage:"
    echo "\$ cd <directory you want to repair>"
    echo "\$ repair-perms.sh"
    echo "Or:"
    echo "\$ repair-perms.sh <directory>"
    exit 0
fi

export target=$1

if [ -z "$target" ] ; then
	export target=`pwd`/
else
	export target=`readlink -f "$target"`
fi

if [[ "$target" != "/kolos/"* && "$target" != "/tytan/"* ]]; then
	echo Cannot repair permissions outside /kolos/ or /tytan/
	exit 1
fi

echo Repairing permissions for $target

trap 'echo KILLING JOBS... && kill $(jobs -p)' SIGINT SIGTERM

chgrp -R users $target &
#chmod -R u+rwX,g+rwXs,o-w $target &
find $target -type f -exec chmod u+rw,g+rw,o-w {} + &
find $target -type d -exec chmod u+rwx,g+rwxs,o-w {} + &

wait

echo Done.

