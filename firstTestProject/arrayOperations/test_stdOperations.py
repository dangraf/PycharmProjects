from unittest import TestCase
import stdOperations as std
import numpy as np
import pandas as pd


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
        print result

        # vefiry
        self.assertEqual(result[4], 0.0)
        self.assertEqual(result[2], 1.0)

