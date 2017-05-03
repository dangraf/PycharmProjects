import pandas as pd
import numpy as np
import pickle

""" takes two vectors that are normalized (length=1)"""
def distAngle(a,b):
    return np.dot(a.values, b.values)

def euclidDist(a,b):
    return (a-b)**2


class mitCluster():
    def __init__(self):
        self.model = None
        self.distances = None
        print("init")

    def loadModel(self,filename):
        self.model = pd.read_pickle(filename)
    def euclidDist(self,a,b):
        temp = (a.values - b.values) ** 2
        return np.sum(temp)


    def saveDistances(self,filename):
        pickle.dump(self.distances,open( filename, "wb" ))

    def loadDistances(self,filename):
        self.distances = pickle.load(open(filename,"rb"))
    """
    df: dataframe containing the data to be clustered
    tresh_h, high treshold, defining limit for when to buy
    tresh_l, low treshold, defining the limit for when to sell.
    trade_win_size: how many samples ahead we shall look
    """
    def calcDistances(self, df, windowsize):
        end = len(df)-windowsize+1
        self.distances = np.zeros([end, end])
        for i in range(0, end):
            slize = df['data'].iloc[i:i+windowsize]
            for j in range(i,end):
                slize2 = df['data'].iloc[j:j + windowsize]
                dist =self.euclidDist(slize, slize2)
                self.distances[i,j] = dist
                self.distances[j, i] = dist
        return self.distances


    def calcOutputVector(self,df, tresh_H, tresh_L, trade_win_size):
        df['max'] = df[::-1].rolling(window=trade_win_size).max()
        df['min'] = df[::-1].rolling(window=trade_win_size).min()

        df['buy'] = df['max'] > tresh_H
        df['sell'] = df['min'] < tresh_L






