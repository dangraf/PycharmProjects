import unittest
import importCSV
import numpy as np
import ConfigParser
import pandas as pd
import math



class TestSequenceFunctions(unittest.TestCase):

    def testFutureData(self):

        fakePrice = np.array(range(1,16))  # 0-14
        fakevolume=  np.array(range(15))
        fakeDate = np.array(range(15))

        dataFrame = pd.DataFrame({'price':fakePrice}, index = fakeDate)
        dataFrame['volume'] = pd.Series(fakevolume,index = fakeDate)

        myfilter = np.array([0, 0.5,0.5])
        myfilter = myfilter[::-1]

        retFr = importCSV.getFutureFiltered( dataFrame,myfilter )


        #check that length of dataframe is unchenged
        self.assertEqual(len(retFr),15)
        filteredFrame = retFr[np.isfinite(retFr['FutureFilter'])]
        # Checking length and content of returned vectors
        self.assertEqual( len(filteredFrame['FutureFilter']), 13)
        self.assertEqual( retFr['price'][12], 13)
        self.assertEqual( retFr['volume'][12], 12)


        # Checking resulting vector
        self.assertEqual( retFr['FutureFilter'][0], 1.5) ## (2+3)/2 = 2.5 = > 2.5/1 - 1.0 = 1.5
        self.assertEqual( retFr['FutureFilter'][12], 14.5/13-1.0) ## (2+3)/2 = 14.5 = > 14.5/13 - 1.0 = 1.5


    def testHistData(self):
        fakePrice = np.array(range(1,16))  # 1-15
        fakevolume=  np.array(range(15))
        fakeDate = np.array(range(15))
        myfilter = np.array([0.5,0.5,0])
        myfilter = myfilter[::-1]

        dataframe =  pd.DataFrame( columns=['price', 'volume','date'])
        dataframe['price'] = fakePrice
        dataframe['volume'] = fakevolume
        dataframe['date'] = fakeDate

        df = importCSV.getHistoryFiltered( dataframe,myfilter )

        # Checking length and content of returned vectors
        self.assertEqual( len(df['HistoryFilter']), 15)
        self.assertTrue( math.isnan(df['HistoryFilter'][0]))
        self.assertTrue(math.isnan(df['HistoryFilter'][1]))
        print df['HistoryFilter']

        # Checking resulting vector
        self.assertEqual( df['HistoryFilter'][2], -0.5) ## (1+2)/2 = 1.5 = > 1.5/3 - 1.0 = 0.5
        self.assertEqual( df['HistoryFilter'][14], 13.5/15-1.0) ## (14+13)/2 = 13.5 = > 15/13.5- 1.0 = 1.5

    def testFutureFilter(self):
        f = importCSV.getFutureFilter([2,4,6,8])
        self.assertEqual( len(f), 9)
        self.assertEqual( f[-2], 0.25)
        self.assertEqual( f[-4], 0.25)
        self.assertEqual( f[-6], 0.25)
        self.assertEqual( f[-8], 0.25)
        self.assertEqual( np.sum(f), 1.0)

    def testUseFutureFilter(self):

        price = range(1,20)
        volume = range(1,20)
        timestamp = range(0,19)

        dataFrame = pd.DataFrame({'price':price}, index = timestamp)
        dataFrame['volume'] = pd.Series(volume,index = timestamp)

        myfilter = importCSV.getFutureFilter([1,3,5])
        newFrame = importCSV.getFutureFiltered( dataFrame,myfilter )


        length = len(newFrame['price'])-len(myfilter)

        for i in range(length):
            meanP = (price[i+1] + price[i+3] + price[i+5])/3.0
            change = meanP/price[i]-1.0;
            self.assertAlmostEqual(change, newFrame['FutureFilter'][i])
            i = i+1;

    def testUseHistFilter(self):
        price = range(1,20)
        volume = range(1,20)
        timestamp = range(1,20)
        dataFrame = pd.DataFrame({'price':price,'volume':volume}, index = timestamp)

        myfilter = importCSV.getHistoryFilter([5,4,2])
        retFrame = importCSV.getHistoryFiltered( dataFrame,myfilter )

        i = 0;
        for i in range(5,len(retFrame)):
            meanP = (price[i-5] + price[i-4] + price[i-2])/3.0
            change = meanP/price[i]-1.0;
            print change
            print retFrame['HistoryFilter'].iloc[i]
            self.assertAlmostEqual(change, retFrame['HistoryFilter'].iloc[i])
            i = i+1;

    def testParseOrderdepth(self):

        config = ConfigParser.ConfigParser()
        config.read('config.cfg')

        filename = config.get('Section1', 'orderdepthfilename')
        directory = config.get('Section1', 'bitcoinHistDataFolder')
        a = importCSV.getOrderDepthRatio(directory+filename, 60)
        size = np.shape(a)
        self.assertEqual(size[1], 1)
        self.assertEqual(size[0], 613)
        indexes = a.index

        startTime = indexes[0]
        a = np.array(a)
        indexes  = a[:,0] - startTime


        frame = pd.DataFrame(a)
        frame.to_csv('test.csv')



if __name__ == '__main__':
    unittest.main()