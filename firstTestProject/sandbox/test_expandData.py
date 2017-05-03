from unittest import TestCase
import expandData as ex
import numpy as np

class TestExpandData(TestCase):
    def test_expandData(self):
        X = np.array([1,2,3,4,5])
        y = ex.expandData(X)

        print(X)
        [a, b] = np.shape(y)
        self.assertEquals(a, 3)
        self.assertEquals(b, 3)

    def test_exapndDoubleData(self):
        X = np.arange(10).reshape(5,2)
        y = ex.expandData(X)
        print(X[1,:])
        self.fail()
