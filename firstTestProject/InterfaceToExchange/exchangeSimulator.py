import exchangeBase
import pandas as pd
import numpy as np
import types



class exchangeSimulator(exchangeBase):

    def __init__(self, BTCAmount, DollarAmount ):
        assert isinstance(BTCAmount, types.FloatType)
        self.Btc = BTCAmount
        assert isinstance(DollarAmount, types.FloatType)
        self.Cash = DollarAmount
        self.BuyBook = np.empty(shape=(0,3))
        self.SellBook = np.empty(shape=(0,3))
        self.tickCounter = 0
        self.lastBtcPrice = 1
        self.BtcAccess = BTCAmount
        self.CashAccess = DollarAmount
        self.CNTR_IDX = 0
        self.PRICE_IDX = 1
        self.VOLUME_IDX = 2
        self.dataframe = pd.DataFrame({'tick','price','buyTime','sellTime'})

    # private function, calculates the total amount of presented in both BTC and Cash
    def updateAccessValues(self):
        self.BtcAccess = self.Btc
        self.CashAccess = self.Cash
        for i in range(len(self.SellBook)):
            self.BtcAccess = self.BtcAccess - self.SellBook[i, self.VOLUME_IDX]

        for i in range(len(self.BuyBook)):
            self.CashAccess = self.CashAccess - self.BuyBook[i, self.PRICE_IDX] * self.BuyBook[i, self.VOLUME_IDX]

    #def calcTresholdInBtc(self, volumeInPercent):
    #    assets = self.Cash / self.lastBtcPrice + self.Btc
    #    return assets * volumeInPercent

    def getAssetsInBtc(self, price):
        return self.Btc + self.Cash / price

    # deletes orders older than the timestamp of "ticktime"
    def clearOldOrders(self, tickTime):
        timeLimit = self.tickCounter - tickTime

        indexToDelete = np.where(self.BuyBook[:, 0] < timeLimit)
        self.BuyBook = np.delete(self.BuyBook, indexToDelete, axis=0)

        indexToDelete = np.where(self.SellBook[:, 0] < timeLimit)
        self.SellBook = np.delete(self.SellBook, indexToDelete, axis=0)

    def buy(self, BtcPrice, Volume):
        if Volume * BtcPrice < self.CashAccess:
            #            print('Order, Selling {0}Btc at price {1}'.format(Volume,BtcPrice))
            self.BuyBook = np.vstack([self.BuyBook, [self.tickCounter, BtcPrice, Volume]])
            self.updateAccessValues()

    def sell(self, BtcPrice, Volume):
        if Volume < self.BtcAccess:
            #            print('Order, Selling {0}Btc at price {1}'.format(Volume,BtcPrice))
            self.SellBook = np.vstack([self.SellBook, [self.tickCounter, BtcPrice, Volume]])
            self.updateAccessValues()