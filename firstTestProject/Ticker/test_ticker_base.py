from unittest import TestCase
import ticker_base as  tb
import datetime as dt

class TestTicker_base(TestCase):
    def test_init_update_period(self):

        tick = tb.ticker_base('unittest',updatePeriodS=1,url='https:\\test')
        time_start = dt.datetime.now()
        tick.waitUntilNextUpdate()
        time_end = dt.datetime.now()

        exectime = time_end - time_start
        self.assertAlmostEqual(1,exectime.total_seconds(),delta=0.01 )

    def test_second_update_period(self):
        tick = tb.ticker_base('unittest', updatePeriodS=1, url='https:\\test')
        time_start = dt.datetime.now()
        tick.waitUntilNextUpdate()
        tick.waitUntilNextUpdate()
        time_end = dt.datetime.now()

        exectime = time_end - time_start
        self.assertAlmostEqual(2, exectime.total_seconds(), delta=0.01)

    def test_market_cap_ticker(self):
        tick = tb.ticker_base('unittest', updatePeriodS=1, url='https://api.coinmarketcap.com/v1/ticker/?limit = 5')
        time_start = dt.datetime.now()
        tick.waitUntilNextUpdate()

    def test_get_failing_url(self):
        tick = tb.ticker_base('unittest', updatePeriodS=1, url='https:\\test')
        tick.getData()
        # test shall not break
        pass

    def test_get_coinmarketcap_url(self):
        tick = tb.ticker_base('unittest', updatePeriodS=1, url='https://api.coinmarketcap.com/v1/ticker/?limit=5')
        data = tick.getData()
        a = len(data)
        self.assertEqual(a,5)
    def test_append_dataframe(self):
        tick = tb.ticker_base('unittest', updatePeriodS=1, url='https://api.coinmarketcap.com/v1/ticker/?limit=5')
        data = tick.getData()
        data = tick.getData()
        a = len(data)
        self.assertEqual(a, 5)


