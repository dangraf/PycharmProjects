from unittest import TestCase
import exchangeSimulator as exSim


__author__ = 'Daniel Grafstrom'
__project__ = 'InterfaceToExchange'

class TestExchangeSimulator(TestCase):

    def setupSimulator(self):
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

    def testDemp(self):

        # setup
        # test
        # verify
        pass

