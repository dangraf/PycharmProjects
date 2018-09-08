from unittest import TestCase
from unittest.mock import patch
from Ticker.data_getters import *
from Projects.mongo_data import init_mongodb


class TestGetCoinmarketcap(TestCase):

    @patch('Ticker.data_getters.mongo')
    def test_coinmarketcap(self, mock_mongo):
        # test
        get_coinmarketcap()
        # verify
        self.assertTrue(mock_mongo.save_tickerdata.called)
        colname = mock_mongo.save_tickerdata.call_args[1]['collection_name']
        data = mock_mongo.save_tickerdata.call_args[1]['data']
        self.assertEqual(colname, 'coinmarketcap_top100')
        self.assertEqual(len(data), 100)

    @patch('Ticker.data_getters.mongo')
    def test_globalcap(self, mock_mongo):
        # test
        get_global_cap()
        # verify
        self.assertTrue(mock_mongo.save_tickerdata.called)
        colname = mock_mongo.save_tickerdata.call_args[1]['collection_name']
        data = mock_mongo.save_tickerdata.call_args[1]['data']
        self.assertEqual(colname, 'global_market')
        self.assertEqual(len(data), 7)

    @patch('Ticker.data_getters.mongo')
    def test_bitcoin_fees(self, mock_mongo):
        get_bitcoin_fees()
        self.assertTrue(mock_mongo.save_tickerdata.called)
        colname = mock_mongo.save_tickerdata.call_args[1]['collection_name']
        data = mock_mongo.save_tickerdata.call_args[1]['data']
        self.assertEqual(colname, 'bitcoin_fees')
        self.assertEqual(len(data), 3)

    @patch('Ticker.data_getters.mongo')
    def test_bitcoinaverage_ticker(self, mock_mongo):
        get_bitcoinaverage_ticker_data()
        self.assertTrue(mock_mongo.save_tickerdata.called)
        colname = mock_mongo.save_tickerdata.call_args[1]['collection_name']
        data = mock_mongo.save_tickerdata.call_args[1]['data']
        self.assertEqual(colname, 'bitcoinaverage_ticker')
        self.assertEqual(len(data), 12)

    @patch('Ticker.data_getters.mongo')
    def test_bitcoincharts(self, mock_mongo):
        get_bitcoincharts_data()
        self.assertTrue(mock_mongo.save_tickerdata.called)
        colname = mock_mongo.save_tickerdata.call_args[1]['collection_name']
        data = mock_mongo.save_tickerdata.call_args[1]['data']
        self.assertEqual(colname, 'bitcoincharts_global')
        self.assertEqual(len(data), 3)



    def test_get_news_data(self):
        init_mongodb()
        get_news_data()
