from vision.config.main import *


@apply_config
class config(config):
    class paths(Config):
        home = '/tytan/raid'
        cnn_models_home = '{paths.home}/cnn-models'
        default_caffe = '{caffe.default_home}'

    class caffe(Config):
        default_home = '~/caffe/python'
        default_ssd = '~/caffe-ssd/python'
        default_pva = '~/caffe-pva/caffe-fast-rcnn/python'
        default_gpu = 0

    class rcnn(Config):
        caffe_path = '{caffe.default_home}'
        use_cpu = False
        gpu_id = 0
        cnn_type = 'VGG16'
        deploy = '{paths.cnn_models_home}/faster_rcnn-voc/{cnn_type}_faster_rcnn_test.pt'
        model = '{paths.cnn_models_home}/faster_rcnn-voc/{cnn_type}_faster_rcnn_final.caffemodel'
        classes = '{paths.cnn_models_home}/faster_rcnn-voc/classes.json'

