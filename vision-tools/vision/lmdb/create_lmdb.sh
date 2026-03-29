#!/usr/bin/env bash
# Create the lmdb files

# paths to caffe tools
export PATH=$PATH:/opt/caffe/bin:~/caffe/distribute/bin

[ -z "$VISION_TOOLS" ] && export VISION_TOOLS=~/repos/vision-tools/vision/lmdb

[ -z "$DATA_ROOT" ] && export DATA_ROOT=/
[ -z "$LISTS" ] && export LISTS=`pwd`
[ -z "$DEST" ] && export DEST=$LISTS
[ -z "$SHUFFLE" ] && export SHUFFLE=true
[ -z "$CALC_MEAN" ] && export CALC_MEAN=yes

[ -z "$RESIZE" ] && export RESIZE=227
[ -z "$RESIZE_HEIGHT" ] && export RESIZE_HEIGHT=$RESIZE
[ -z "$RESIZE_WIDTH" ] && export RESIZE_WIDTH=$RESIZE


if [ ! -d "$DATA_ROOT" ]; then
  echo "Error: DATA_ROOT is not a path to a directory: $DATA_ROOT"
  echo "Set the DATA_ROOT variable in create_lmdb.sh to the path" \
       "where the data is stored."
  exit 1
fi


LAST_DIR=`pwd`
cd $LISTS

for file in `ls *.txt`
do

    file=${file/.txt/}

    if [[ "$file" == "names" ]]; then
        continue
    fi

    echo "Creating "$file" lmdb... (resize=$RESIZE_HEIGHT:$RESIZE_WIDTH, shuffle=$SHUFFLE)"

    if [ -e $DEST/${file}_lmdb ]; then
        rm -r $DEST/${file}_lmdb
    fi

    GLOG_logtostderr=1 convert_imageset.bin \
        --resize_height=$RESIZE_HEIGHT \
        --resize_width=$RESIZE_WIDTH \
        --shuffle=$SHUFFLE \
        $DATA_ROOT \
        $LISTS/${file}.txt \
        $DEST/${file}_lmdb &
done

wait

echo "All LMDBs created for $LISTS"

cd $LAST_DIR

[[ "$CALC_MEAN" == "yes" ]] && $VISION_TOOLS/calc_mean.sh

echo "Done."
