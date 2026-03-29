import cv2
import numpy as np
from matplotlib import pyplot as plt, gridspec, cm

from vision.helpers.file_helpers import find_all_images


def plot_image(img, ax, title):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ax.set_title(title)
    ax.set_aspect("equal", "box-forced")
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    ax.imshow(img, extent=[-img.shape[1]/2., img.shape[1]/2., -img.shape[0]/2., img.shape[0]/2.])


def plot_output(result, ax, names):
    ax.bar(np.arange(0, result.shape[0]), result)
    ax.set_title("Network output")
    ax.set_ylim(0, 1)
    ax.set_xticks(np.arange(0, result.shape[0]))
    ax.set_xticklabels(names, rotation="vertical")
    ax.margins(0)


def plot_threshold(ax, thresh, color="r"):
    ax.axhline(thresh, lw=0.5, color=color)


def plot_network_for_image(img, input_img, attention_image, result, class_names):
    fig = plt.figure(11546, figsize=(12, 8))

    gs = gridspec.GridSpec(2, 3)

    ax1 = plt.subplot(gs[0, 0])
    ax2 = plt.subplot(gs[0, 1], sharey=ax1, sharex=ax1)
    ax3 = plt.subplot(gs[0, 2], sharey=ax1, sharex=ax1)
    ax4 = plt.subplot(gs[1, :])

    plot_image(img, ax1, "Original image")
    plot_image(input_img, ax2, "Network input")
    plot_image(attention_image, ax3, "Attention map")

    plot_threshold(ax4, 0.5)
    plot_threshold(ax4, 0.9, color="g")

    plot_output(result, ax4, class_names)

    fig.tight_layout()

    plt.show(block=False)
    # need to redrawn figure
    plt.pause(0.1)


def wait_for_keyboard():
    while not plt.waitforbuttonpress():
        pass


def get_last_activation_layer_idx(model):
    from vis.utils import utils
    for idx, layer in utils.reverse_enumerate(model.layers):
        if "activation" in layer.get_config():
            return idx

    return None


def get_modified_model(model):
    from keras import activations
    from keras.applications import mobilenet
    from vis.utils import utils

    layer_idx = get_last_activation_layer_idx(model)
    model.layers[layer_idx].activation = activations.linear

    objects = None
    if model.name == "mobilenet":
        objects = {"relu6": mobilenet.relu6}
    modified_model = utils.apply_modifications(model, custom_objects=objects)
    modified_model.layers[layer_idx + 1:] = []
    return modified_model


def debug_network(network, modified_model, images, class_names):
    from vis import visualization as vis

    for img in images:
        input_img = network.prepare([img])[0]
        result = network.model.predict(np.array([input_img]))[0]

        if np.max(result) > 0.1:
            grads = vis.visualize_cam(modified_model, -1, filter_indices=np.argmax(result), seed_input=input_img, backprop_modifier=None)
        else:
            grads = np.full(input_img.shape[:2], 0.0, dtype=np.float32)

        heatmap = np.flip(np.uint8(cm.jet(grads)[..., :3] * 255), axis=2)
        attention_img = vis.overlay(heatmap, input_img)
        plot_network_for_image(img, input_img, attention_img, result, class_names)
        wait_for_keyboard()


def debug(test_dir, network_params, class_names):
    from vision.keras.models.networks import GeneralNeuralNetwork

    network = GeneralNeuralNetwork(*network_params)
    modified_model = get_modified_model(network.model)

    paths = find_all_images(test_dir)
    images = [cv2.imread(path) for path in paths]
    debug_network(network, modified_model, images, class_names)
