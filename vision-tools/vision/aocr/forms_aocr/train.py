from __future__ import absolute_import

from vision.aocr.forms_aocr.config import config
from vision.aocr.api import AOCR_Train


if __name__ == '__main__':
    config = config.forms.jachootest
    aocr = AOCR_Train(config)
    aocr.train()
