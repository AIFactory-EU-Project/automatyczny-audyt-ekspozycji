from .dotted_pipelines import *
from .embossed_pipelines import *
from .printed_pipelines import *
from .front_face_pipelines import *

__all__ = [
    # dotted pipelines
    "DottedBackgroundPipeline",
    "DottedTextPipeline",

    # embossed pipelines
    "EmbossedTextPipeline",

    # printed pipelines
    "PrintedBackgroundPipeline",
    "PrintedTextPipeline",

    # front face pipelines
    "FrontFaceCompositePipeline",
    "FrontFaceForegroundPipeline"
]
