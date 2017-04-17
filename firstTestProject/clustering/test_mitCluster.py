from unittest import TestCase
import pandas as pd
import mitcluster as mt
import numpy as np

a = np.array([1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 2.0, 3.0, 4.0],dtype=np.float64)
df = pd.DataFrame(a,columns=['data'])
class TestMitCluster(TestCase):
    def test_calcDistance(self):
        obj = mt.mitCluster()
        obj.calcDistance(df,3)
        self.fail()

