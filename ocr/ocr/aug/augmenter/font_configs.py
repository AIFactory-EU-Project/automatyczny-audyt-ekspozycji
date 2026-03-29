import importlib


class FontConfig:
    def __init__(self, op_type="crop"):
        self.op_type = op_type
        self.op_module = importlib.import_module(f"ocr.aug.transformations.configs.{self.op_type}")
        self.background_ops = None
        self.composite_ops = None
        self.foreground_ops = None
        self.text_ops = None

    def load_ops(self, class_to_load):
        try:
            ops = getattr(self.op_module, class_to_load)()
        # when no such module is found, return None
        except AttributeError:
            ops = None

        return ops


class DottedConfig(FontConfig):
    def __init__(self, op_type):
        super(DottedConfig, self).__init__(op_type)
        self.background_ops = self.load_ops("DottedBackgroundPipeline")
        self.composite_ops = self.load_ops("DottedCompositePipeline")
        self.foreground_ops = self.load_ops("DottedForegroundPipeline")
        self.text_ops = self.load_ops("DottedTextPipeline")


class EmbossedConfig(FontConfig):
    def __init__(self, op_type):
        super(EmbossedConfig, self).__init__(op_type)
        self.background_ops = self.load_ops("EmbossedBackgroundPipeline")
        self.composite_ops = self.load_ops("EmbossedCompositePipeline")
        self.foreground_ops = self.load_ops("EmbossedForegroundPipeline")
        self.text_ops = self.load_ops("EmbossedTextPipeline")


class PrintedConfig(FontConfig):
    def __init__(self, op_type):
        super(PrintedConfig, self).__init__(op_type)
        self.background_ops = self.load_ops("PrintedBackgroundPipeline")
        self.composite_ops = self.load_ops("PrintedCompositePipeline")
        self.foreground_ops = self.load_ops("PrintedForegroundPipeline")
        self.text_ops = self.load_ops("PrintedTextPipeline")


class FrontFaceConfig(FontConfig):
    def __init__(self, op_type):
        super(FrontFaceConfig, self).__init__(op_type)
        self.background_ops = self.load_ops("FrontFaceBackgroundPipeline")
        self.composite_ops = self.load_ops("FrontFaceCompositePipeline")
        self.foreground_ops = self.load_ops("FrontFaceForegroundPipeline")
        self.text_ops = self.load_ops("FrontFaceTextPipeline")
