from unittest import TestCase
import Ticker as tk


class TestTicker(TestCase):
    def test_PrepareFile(self):
        tick = tk.ticker()
        tick.PrepareFile('1mintestdata.csv')
        self.assertTrue(True)

    def test_VerifWeHaveDataForEachSecond(self):
        tick = tk.ticker()
        tick.PrepareFile('1mintestdata.csv')
        startDate = tick.Data.index[0]
        endDate = tick.Data.index[-1]
        dataSize = len(tick.Data['price'])
        numSeconds = endDate - startDate
        min =(numSeconds + 1)/60


        self.assertEqual(min, dataSize)
