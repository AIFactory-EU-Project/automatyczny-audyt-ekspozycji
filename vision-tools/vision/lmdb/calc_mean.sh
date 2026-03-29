#!/usr/bin/env bash
# Compute the mean images

# paths to caffe tools
export PATH=$PATH:/opt/caffe/bin:~/caffe/distribute/bin

[ -z "$VISION_TOOLS" ] && export VISION_TOOLS=~/repos/vision/vision/endo/data/tools

[ -z "$LISTS" ] && LISTS=/tytan/raid/fashion/categorization/lmdb/T2-amazon/lmdb-pattern-crops-2
[ -z "$DEST" ] && DEST=$LISTS


cd $LISTS

for FILE in `ls *.txt`
do
    FILE=${FILE/.txt/}
    if [[ "$FILE" == "names" ]]; then
        continue
    fi
    echo Calculating mean for: $FILE
    compute_image_mean.bin $LISTS/${FILE}_lmdb $DEST/${FILE}_mean.binaryproto &
done

wait

echo "Mean calculation done."

