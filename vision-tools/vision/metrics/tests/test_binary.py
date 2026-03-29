from __future__ import absolute_import
import unittest
import numpy as np
from vision.metrics.numpy import binary


class TestBinary(unittest.TestCase):

    def test_auc(self):
        gt = np.array([0, 0, 1, 1])
        pred = np.array([0.1, 0.4, 0.35, 0.8])
        auc = binary.roc_auc(pred, gt)
        self.assertAlmostEquals(auc, 0.75)


if __name__ == '__main__':
    unittest.main()
