from unittest import TestCase
import pandas as pd
import mitcluster as mt
import numpy as np
import os

#globals
a = np.array([1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=np.float64)
df = pd.DataFrame(a,columns=['data'])
filename = 'unittestFile.p'

class TestMitCluster(TestCase):
    def test_calcDistance(self):
        obj = mt.mitCluster()
        result = obj.calcDistances(df,3)
        B,H = np.shape(result)
        expLen = len(df)-2
        self.assertEqual(B, expLen)
        self.assertEqual(H, expLen)

    def test_SaveDistance(self):
        # prepare
        if os.path.isfile(filename):
            os.remove(filename)

        obj = mt.mitCluster()
        obj.calcDistances(df, 3)

        #test
        obj.saveDistances(filename)

        # verify
        if not os.path.isfile(filename):
            self.fail()

    def test_loadDistance(self):

        # prepare
        obj = mt.mitCluster()
        if not obj.distances== None:
            self.fail()
        if not os.path.isfile(filename):
            self.fail()

        # test
        obj.loadDistances(filename)

        #verify
        B, H = np.shape(obj.distances)
        self.assertEqual(B, 8)
        self.assertEqual(H, 8)






