from unittest import TestCase
import neural as n

class TestNeural(TestCase):
    def testInit(self):
        net = n.Neural([2, 3, 2])
        self.assertEquals(len(net.biases),3)
    pass
