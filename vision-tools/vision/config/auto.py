from vision.config.main import *
from vision.config.defaults import *

try:
    import vision.config.local
except ImportError:
    pass


config.process_references()


__all__ = ["config", "auto_config", "Config"]

