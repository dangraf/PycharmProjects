import exchangeBase as eb
import pandas as pd
import numpy as np
import types


class exchangeSimulator(eb.exchangeBase):
    Btc = 0.0
    Cash= 0.0
    BuyBook = np.empty(shape=(0, 3))
    SellBook = np.empty(shape=(0, 3))
    # BTCAmount: number of bitcoins on the account at startup
    # DollarAmount: number of dollars on the account at startup
    # tradeFee: tradeFee  eg 0.002 represent a fee at 0.2% for both selling and buying
    def __init__(self, BTCAmount, DollarAmount):
        assert isinstance(BTCAmount, types.FloatType)
        self.Btc = BTCAmount
        assert isinstance(DollarAmount, types.FloatType)
        self.Cash = DollarAmount
       # self.BuyBook = np.empty(shape=(0, 3))
        #self.SellBook = np.empty(shape=(0, 3))
        self.tickCounter = 0
        self.lastBtcPrice = 1
        self.BtcAccess = BTCAmount
        self.CashAccess = DollarAmount
        self.CNTR_IDX = 0
        self.PRICE_IDX = 1
        self.VOLUME_IDX = 2
        self.tradefee = 0

        self.dataframe = pd.DataFrame(columns =['tick', 'price', 'buyTime', 'sellTime'])

    def initialize(self, tradeFee):
        self.tradefee = tradeFee

    # private function, calculates the total amount of presented in both BTC and Cash
    def updateAccessValues(self):
        self.BtcAccess = self.Btc
        self.CashAccess = self.Cash
        for i in range(len(self.SellBook)):
            self.BtcAccess = self.BtcAccess - self.SellBook[i, self.VOLUME_IDX]

        for i in range(len(self.BuyBook)):
            self.CashAccess = self.CashAccess - self.BuyBook[i, self.PRICE_IDX] * self.BuyBook[i, self.VOLUME_IDX]

    # def calcTresholdInBtc(self, volumeInPercent):
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

    def tickEvent(self, price, volume):
        CNTR_IDX = 0
        PRICE_IDX = 1
        VOLUME_IDX = 2
        lastBtcPrice = price
        i = 0;
        while (i < len(self.BuyBook)):
            if (price <= self.BuyBook[i][PRICE_IDX] and price * self.BuyBook[i][VOLUME_IDX] < self.Cash):
                #                print('Buying {0}Btc at price {1}'.format(self.BuyBook[i][VOLUME_IDX],price))
                self.Btc = self.Btc + self.BuyBook[i][VOLUME_IDX]
                self.Cash = self.Cash - price * self.BuyBook[i][VOLUME_IDX]
                self.BuyBook = np.delete(self.BuyBook, i, axis=0)
                self.updateAccessValues()

            else:
                i = i + 1
        i = 0
        while (i < len(self.SellBook)):
            if (price >= self.SellBook[i][PRICE_IDX] and self.SellBook[i][VOLUME_IDX] < self.Btc):
                #                print('Selling {0}Btc at price {1}'.format(self.SellBook[i][VOLUME_IDX],price))
                self.Btc = self.Btc - self.SellBook[i][VOLUME_IDX]
                self.Cash = self.Cash + price * self.SellBook[i][VOLUME_IDX]
                self.SellBook = np.delete(self.SellBook, i, axis=0)
                self.updateAccessValues()

            else:
                i = i + 1
        self.tickCounter = self.tickCounter + 1
        self.dataframe['tick'].append(self.tickCounter)
        self.dataframe['price'].append(price)

    def cancel(self, orderID):
        # canceles an order
        return

    def getAccountInfo(self):
        # returns: balance, BTC, $
        return

    def getOrderDepth(self, depth):
        # returns orderdepth
        return
