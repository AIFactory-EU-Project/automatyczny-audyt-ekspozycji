class TFDetectorConfig:

    def __init__(self, graph_path, labels_path, input_size, detection_threshold, gpu_memory_fraction):
        self.graph_path = graph_path
        self.labels_path = labels_path
        self.input_size = input_size
        self.detection_threshold = detection_threshold
        self.gpu_memory_fraction = gpu_memory_fraction


class KerasClassifierConfig:

    def __init__(self, weights_path, input_size, pad_image, grayscale, model, activation, gpu_memory_fraction):
        self.weights_path = weights_path
        self.input_size = input_size
        self.pad_image = pad_image
        self.grayscale = grayscale
        self.model = model
        self.activation = activation
        self.gpu_memory_fraction = gpu_memory_fraction


class KerasMultiClassifierConfig:

    def __init__(self, classes, configs, thresholds, min_advantage, gpu_memory_fraction):
        self.classes = classes
        self.thresholds = thresholds
        self.min_advantage = min_advantage
        self.configs = configs
        self.gpu_memory_fraction = gpu_memory_fraction


class AOCRConfig:

    def __init__(self, checkpoint_path, gpu_memory_fraction):
        self.checkpoint_path = checkpoint_path
        self.gpu_memory_fraction = gpu_memory_fraction
