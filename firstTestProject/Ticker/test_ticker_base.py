from unittest import TestCase
import tickerbase as tb
import datetime as dt


class TestTicker_base(TestCase):
    def test_init_update_period(self):

        tick = tb.TickerBase('unittest', update_period_s=1, url='https:\\test')
        time_start = dt.datetime.now()
        tick.wait_until_next_update()
        time_end = dt.datetime.now()

        exectime = time_end - time_start
        self.assertAlmostEqual(1, exectime.total_seconds(), delta=0.01 )

    def test_second_update_period(self):
        tick = tb.TickerBase('unittest', update_period_s=1, url='https:\\test')
        time_start = dt.datetime.now()
        tick.wait_until_next_update()
        tick.wait_until_next_update()
        time_end = dt.datetime.now()

        exectime = time_end - time_start
        self.assertAlmostEqual(2, exectime.total_seconds(), delta=0.01)

    def test_market_cap_ticker(self):
        tick = tb.TickerBase('unittest', update_period_s=1, url='https://api.coinmarketcap.com/v1/ticker/?limit = 5')
        time_start = dt.datetime.now()
        tick.wait_until_next_update()

    def test_get_failing_url(self):
        tick = tb.TickerBase('unittest', update_period_s=1, url='https:\\test')
        tick.get_data_save_to_db()
        # test shall not break
        pass

    def test_get_coinmarketcap_url(self):
        tick = tb.TickerBase('unittest', update_period_s=1, url='https://api.coinmarketcap.com/v1/ticker/?limit=5')
        data = tick.get_data_save_to_db()
        a = len(data)
        self.assertEqual(a,5)
    def test_append_dataframe(self):
        tick = tb.TickerBase('unittest', update_period_s=1, url='https://api.coinmarketcap.com/v1/ticker/?limit=5')
        data = tick.get_data_save_to_db()
        data = tick.get_data_save_to_db()
        a = len(data)
        self.assertEqual(a, 5)


