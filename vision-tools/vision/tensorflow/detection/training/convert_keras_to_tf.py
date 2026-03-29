""" Example conversion from Keras to TensorFlow model """

import numpy as np
import cv2

from vision.keras.models.networks import GeneralNeuralNetwork


def main(args):
    from keras import backend as K
    from tensorflow.python.framework import graph_util
    from tensorflow.python.framework import graph_io
    K.set_learning_phase(0)
    weights_path = "/tytan/raid/drugs-counter/trainings/classifier-multilabel-bad-crazy/v6-search/2019-06-28 08:03:35/models/test_f1score_spec-0.973_17_2019-06-28_09-53-52.hdf5"
    img_size = (224, 224, 3)
    classes = 21
    pad_image = True
    grayscale = False
    net = "nasnet"
    activation = "sigmoid"
    network = GeneralNeuralNetwork(weights_path, classes, img_size, pad_image, grayscale, net, activation)
    model = network.model

    output_dir = "/tytan/raid/tmp/converted_models"
    output_model_name = "classifier.pb"

    K.set_image_data_format('channels_last')

    orig_output_node_names = [node.op.name for node in model.outputs]
    converted_output_node_names = orig_output_node_names

    sess = K.get_session()

    constant_graph = graph_util.convert_variables_to_constants(
        sess,
        sess.graph.as_graph_def(),
        converted_output_node_names)

    graph_io.write_graph(constant_graph, output_dir, output_model_name, as_text=False)


def run_test():
    from vision.tensorflow import gpus
    gpus.tensorflow_use_gpus(1)
    import tensorflow as tf

    graph = tf.Graph()
    with graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile("/tytan/raid/tmp/converted_models/classifier.pb", 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    session = tf.Session(graph=graph)
    # Resize to model input size
    img = cv2.imread("/tytan/raid/drugs-counter/data/faces/Aspirin/Aspirin-Pro.png")
    resized = cv2.resize(img, (224, 224))
    # Preprocess and add batch dimension
    input_data = np.array([resized])
    # Run model

    def one_of(names):
        """
        Return the operation name that actually exists in the graph.
        :param names: canditate names
        :return: operation name that exists in the graph
        """
        for name in names:
            operation_names = [o.name for o in session.graph.get_operations()]
            if name.replace(':0', '') in operation_names:
                return name

    input_name = one_of(["input_1:0"])
    output_name = one_of(["reshape_2/Reshape:0"])
    output = session.run(
        output_name,
        {
            input_name: input_data,
        })

    # Unpack from batch
    output = output[0]
    print(output)


def convert_to_tf():
    from vision.tensorflow import gpus
    gpus.tensorflow_use_gpus(-1)
    from tensorflow import app
    app.run(main)


def convert_to_coreml():
    from vision.tensorflow import gpus
    gpus.tensorflow_use_gpus(1)
    import tensorflow as tf
    import tfcoreml as tf_converter

    # to work properly change source code of tfcoreml's function _convert_pb_to_mlmodel
    # replace computing unused_ops and effectively_constant_ops with arrays provided below
    # unused_ops = ['reshape_1/Shape', 'reshape_1/strided_slice/stack', 'reshape_1/strided_slice/stack_1', 'reshape_1/strided_slice/stack_2', 'reshape_1/strided_slice', 'reshape_1/Reshape/shape/1',
    #            'reshape_1/Reshape/shape/2', 'reshape_1/Reshape/shape/3', 'reshape_2/Shape', 'reshape_2/strided_slice/stack', 'reshape_2/strided_slice/stack_1', 'reshape_2/strided_slice/stack_2',
    #            'reshape_2/strided_slice', 'reshape_2/Reshape/shape/1']
    # effectively_constant_ops = ['reshape_2/Reshape/shape', 'reshape_1/Reshape/shape']

    tf_converter.convert(tf_model_path="/tytan/raid/tmp/converted_models/classifier.pb",
                         mlmodel_path="/tytan/raid/tmp/converted_models/Classifier.mlmodel",
                         image_input_names='data',
                         input_name_shape_dict={'input_1:0': [1, 224, 224, 3]},
                         output_feature_names=['dense_sigmoid/Sigmoid:0'])


if __name__ == "__main__":
    # convert_to_tf()
    convert_to_coreml()
