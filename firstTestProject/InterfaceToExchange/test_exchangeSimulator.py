from unittest import TestCase
import exchangeSimulator as exSim


__author__ = 'Daniel Grafstrom'
__project__ = 'InterfaceToExchange'

class TestExchangeSimulator(TestCase):

    def test_init_Simulator(self):
        # setup
        # test
        ob = exSim.exchangeSimulator(1.0, 301.0)


        self.assertEqual(ob.Cash,301.0)
        self.assertEqual(ob.Btc, 1.0)

    def test_Buy(self):

        ob = exSim.exchangeSimulator(1.0, 301.0)


        ob.buy(302, 0.5)
        self.assertEqual(len(ob.BuyBook), 1)


        ob.tickEvent(305, 1)
        self.assertEqual(len(ob.BuyBook), 1)
        ob.tickEvent(300, 1)
        self.assertEqual(len(ob.BuyBook), 0)

        self.assertEqual(ob.Btc, 1.5)
        self.assertEqual(ob.Cash, 151)
    def test_BuyFee(self):

        # setup 1% trade fee
        ob = exSim.exchangeSimulator(1.0, 301.0)
        ob.initialize(tradeFee = 0.01)

        #test
        ob.buy(100.0, 1.0  )
        ob.tickEvent(price = 100.0,volume=2.0)

        #verify
        # price 100 + 1%fee = 101 for 1 btc
        self.assertEqual(ob.Cash, 200.0)


    def test_sellFee(self):
        # setup 1% trade fee
        ob = exSim.exchangeSimulator(2.0, 301.0)
        ob.initialize(tradeFee=0.01)

        # test
        ob.sell(100.0, 1.0)
        ob.tickEvent(price=100.0, volume=2.0)

        # verify
        self.assertEqual(ob.Cash, 400.0)

    def test_Sell(self):
        ob = ob = exSim.exchangeSimulator(1.0, 301.0)
        self.assertEqual(ob.Btc, 1.0)
        self.assertEqual(ob.Cash, 301)

        ob.sell(302, 0.5)
        self.assertEqual(len(ob.SellBook), 1)

        ob.tickEvent(301, 1)
        self.assertEqual(len(ob.SellBook), 1)
        ob.tickEvent(310, 1)
        self.assertEqual(len(ob.SellBook), 0)

        self.assertEqual(ob.Btc, 0.5)
        self.assertEqual(ob.Cash, 456)

    def test_RunSimpleSimulation(self):
        btcPrice = [100, 102, 105, 102, 100, 98]
        ob = exSim.exchangeSimulator(1.0, 100.0)
        ob.sell(103, 0.9)
        ob.buy(99, 1.0)

        self.assertEqual(len(ob.SellBook), 1)
        self.assertEqual(len(ob.BuyBook), 1)
        for p in btcPrice:
            ob.tickEvent(p, 2.0)

        self.assertEqual(len(ob.SellBook), 0)
        self.assertEqual(len(ob.BuyBook), 0)

        print ob.getAssetsInBtc(100)



