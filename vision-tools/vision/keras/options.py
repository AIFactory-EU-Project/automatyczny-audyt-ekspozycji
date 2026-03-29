from keras import backend


def set_channels_order(channels_last):
    if channels_last:
        backend.set_image_data_format('channels_last')
    else:
        backend.set_image_data_format('channels_first')


def set_memory_usage(percent):
    import tensorflow as tf
    from keras.backend.tensorflow_backend import set_session
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = percent
    set_session(tf.Session(config=config))
