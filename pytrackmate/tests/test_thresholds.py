import pytest
import math
import numpy as np
from pytrackmate import thresholds

# Many tests here are based off of tests from Scikit-image

class TestSimpleImage:

    def setup_method(self):

        self.image = np.array(
            [
                [0, 0, 1, 3, 5],
                [0, 1, 4, 3, 4],
                [1, 2, 5, 4, 1],
                [2, 4, 5, 2, 1],
                [4, 5, 1, 0, 0],
            ],
            dtype=int,
        )

    def test_get_isodata_thresh(self):
        pass
    
    def test_get_li_thresh(self):
        pass

    def test_get_minimum_thresh(self):
        pass

    def test_get_mean_threshold(self):
        pass

    def test_get_otsu_thresh(self):
        pass

    def test_get_triangle_thresh(self):
        pass

    def test_get_yen_thresh(self):
        pass
