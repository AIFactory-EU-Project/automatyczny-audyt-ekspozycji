To run training:

1. export CUDA_VISIBLE_DEVICES = X, where X is the number of card you want to use
2. cd ~/repos/shelf_retail/shelves/models/GCNet
3. ./tools/dist_train.sh path_to_cfg_file 1, where path_to_cfg_file is e.g. ../detection/grills/cascade_mask_rcnn_r4_gcb_dconv_c3-c5_x101_32x4d_fpn_syncbn_1x.py