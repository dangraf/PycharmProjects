import abc

class exchangeBase():
    @abc.abstractmethod
    def buy(self, BtcPrice, Volume ):
        # puts creates a buy order
        # returns ID other than 0 if order was successfoul
        return

    @abc.abstractmethod
    def sell(self, BtcPrice, Volume):
        # crates a sell order
        # returns ID order ID other than 0 if it was successfoul
        return

    @abc.abstractmethod
    def cancel(self, orderID):
        # canceles an order
        return

    @abc.abstractmethod
    def getAccountInfo(self):
        # returns: balance, BTC, $
        return

    @abc.abstractmethod
    def getOrderDepth(self, depth):
        # returns orderdepth
        return

