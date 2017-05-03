from unittest import TestCase
import stdOperations as std
import numpy as np
#import pandas as pd


__author__ = 'Daniel Grafstrom'
__project__ = 'InterfaceToExchange'

class test_stdOperations(TestCase):

    def test_arrayToPercent(self):
        # setup
        input_array = np.array([10.0, 12.0, 20.0,0.0,-10.0])
        # test
        result = std.arrayToPercent(input_array)

        #vefiry

        self.assertEqual(result[0],00.0)
        self.assertEqual(result[1], 20.0)
        self.assertEqual(result[2], 100.0)
        self.assertEqual(result[3], -100.0)
        self.assertEqual(result[4], -200.0)

    def test_normalize(self):
        # setup
        input_array = np.array([10.0, 12.0, 20.0, 0.0, -10.0])
        # test
        result = std.normalize(input_array)


        # vefiry
        self.assertEqual(result[4], 0.0)
        self.assertEqual(result[2], 1.0)


    def test_expandData(self):
        X = np.array([1, 2, 3, 4, 5])
        y = std.expandData(X)

        print(X)
        [a, b] = np.shape(y)
        self.assertEquals(a, 3)
        self.assertEquals(b, 3)

    def test_exapndCanBeModified(self):
        X = np.arange(10)
        y = std.expandData(X, chunksize=3)

        self.assertEqual(y[1, 2], y[2, 1])
        y[1, 2] = 25
        self.assertNotEqual(y[1,2],y[2,1])


    def test_exapndDoubleData(self):
        X = np.arange(10).reshape(5, 2)
        y = std.expandData(X)
        dims = np.shape(y)
        print(dims)
        self.assertEquals(dims[0], 3)
        self.assertEquals(dims[1], 3)
        self.assertEquals(dims[2], 2)

