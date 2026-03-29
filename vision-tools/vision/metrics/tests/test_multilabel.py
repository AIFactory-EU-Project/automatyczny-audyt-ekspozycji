from __future__ import absolute_import
import unittest
import numpy as np
from vision.metrics.numpy import multilabel


class TestMultilabel(unittest.TestCase):

    gt1 = np.array([[1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1],
                    [1, 1, 0],
                    [1, 0, 1],
                    [0, 1, 1]])

    pred1 = np.array([[1, 0, 1],
                      [0, 1, 0],
                      [0, 0, 1],
                      [0, 0, 1],
                      [0, 0, 0],
                      [0, 1, 1]])

    gt2 = np.array([[1, 0, 0]])
    pred2 = np.array([[0, 0, 0]])

    gt3 = np.array([[1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1],
                    [1, 1, 0],
                    [1, 0, 1],
                    [0, 1, 1]])

    pred3 = np.array([[0.5, 0, 0.8],
                      [0.1, 0.6, 0],
                      [0.1, 0, 0.8],
                      [0, 0.2, 0.8],
                      [0, 0.2, 0.5],
                      [0, 0.6, 0.8]])

    def test_per_class_accuracy(self):
        acc1 = multilabel.accuracy(self.pred1, self.gt1, per_class=True)
        acc2 = multilabel.accuracy(self.pred2, self.gt2, per_class=True)
        np.testing.assert_almost_equal(acc1, [2./3, 5./6, 0.5])
        np.testing.assert_almost_equal(acc2, [0, 1, 1])

    def test_accuracy(self):
        acc1 = multilabel.accuracy(self.pred1, self.gt1)
        acc2 = multilabel.accuracy(self.pred2, self.gt2)
        np.testing.assert_almost_equal(acc1, 2./3)
        np.testing.assert_almost_equal(acc2, 2./3)

    def test_per_class_sensitivity(self):
        sens1 = multilabel.sensitivity(self.pred1, self.gt1, per_class=True)
        sens2 = multilabel.sensitivity(self.pred2, self.gt2, per_class=True)
        np.testing.assert_almost_equal(sens1, [1./3, 2./3, 2./3])
        np.testing.assert_almost_equal(sens2, [0, 0, 0])

    def test_sensitivity(self):
        sens1 = multilabel.sensitivity(self.pred1, self.gt1)
        sens2 = multilabel.sensitivity(self.pred2, self.gt2)
        np.testing.assert_almost_equal(sens1, 5./9)
        np.testing.assert_almost_equal(sens2, 0)

    def test_per_class_specificity(self):
        spec1 = multilabel.specificity(self.pred1, self.gt1, per_class=True)
        spec2 = multilabel.specificity(self.pred2, self.gt2, per_class=True)
        np.testing.assert_almost_equal(spec1, [1, 1, 1./3])
        np.testing.assert_almost_equal(spec2, [0, 1, 1])

    def test_specificity(self):
        spec1 = multilabel.specificity(self.pred1, self.gt1)
        spec2 = multilabel.specificity(self.pred2, self.gt2)
        np.testing.assert_almost_equal(spec1, 7./9)
        np.testing.assert_almost_equal(spec2, 2./3)

    def test_per_class_precision(self):
        prec1 = multilabel.precision(self.pred1, self.gt1, per_class=True)
        prec2 = multilabel.precision(self.pred2, self.gt2, per_class=True)
        np.testing.assert_almost_equal(prec1, [1, 1, 0.5])
        np.testing.assert_almost_equal(prec2, [0, 0, 0])

    def test_precision(self):
        spec1 = multilabel.precision(self.pred1, self.gt1)
        spec2 = multilabel.precision(self.pred2, self.gt2)
        np.testing.assert_almost_equal(spec1, 5./6)
        np.testing.assert_almost_equal(spec2, 0)

    def test_per_class_f1score(self):
        f1score1 = multilabel.f1score(self.pred1, self.gt1, per_class=True)
        f1score2 = multilabel.f1score(self.pred2, self.gt2, per_class=True)
        np.testing.assert_almost_equal(f1score1, [0.5, 0.8, 0.5714286])
        np.testing.assert_almost_equal(f1score2, [0, 0, 0])

    def test_f1score(self):
        f1score1 = multilabel.f1score(self.pred1, self.gt1)
        f1score2 = multilabel.f1score(self.pred2, self.gt2)
        np.testing.assert_almost_equal(f1score1, 0.6238095)
        np.testing.assert_almost_equal(f1score2, 0)

    def test_per_class_f1score_spec(self):
        f1score1 = multilabel.f1score_spec(self.pred1, self.gt1, per_class=True)
        f1score2 = multilabel.f1score_spec(self.pred2, self.gt2, per_class=True)
        np.testing.assert_almost_equal(f1score1, [0.5, 0.8, 0.4444444])
        np.testing.assert_almost_equal(f1score2, [0, 0, 0])

    def test_per_class_variable_threshold_f1score_spec(self):
        f1score3 = multilabel.f1score_spec(self.pred3, self.gt3, threshold=[0.4, 0.5, 0.7], per_class=True)
        f1score2 = multilabel.f1score_spec(self.pred2, self.gt2, threshold=[0.0, 0.4, 0.8], per_class=True)
        np.testing.assert_almost_equal(f1score3, [0.5, 0.8, 0.4444444])
        np.testing.assert_almost_equal(f1score2, [0, 0, 0])

    def test_f1score_spec(self):
        f1score1 = multilabel.f1score_spec(self.pred1, self.gt1)
        f1score2 = multilabel.f1score_spec(self.pred2, self.gt2)
        np.testing.assert_almost_equal(f1score1, 0.5814814)
        np.testing.assert_almost_equal(f1score2, 0)

    def test_auc(self):
        gt = np.array([[0, 0], [0, 0], [1, 1], [1, 1]])
        pred = np.array([[0.1, 0.1], [0.4, 0.4], [0.35, 0.35], [0.8, 0.8]])
        auc = multilabel.roc_auc(pred, gt)
        np.testing.assert_equal(auc, [0.75, 0.75])


if __name__ == '__main__':
    unittest.main()
