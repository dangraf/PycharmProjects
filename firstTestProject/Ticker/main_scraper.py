# -*- coding: utf-8 -*-
"""
Base class for fetching data from a home-page and save it to a mongo-db

_author__ =  "Daniel Grafström"
__license__ = "GPL"
__status__ = "Experimental"
"""

import tickerbase as tb
import _thread
import logging


def create_logger():
    logger = logging.getLogger('main_scraper')
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('main_scraper.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("Main_scraper started")
    logger.debug("Main_scraper started")
    logger.error("Main_scraper started")


# https://apiv2.bitcoinaverage.com/
# http://bitcoincharts.com/about/markets-api/
# https://blockchain.info/api
# https://api.blockchain.info/charts/bitcoin-unlimited-share?timespan=5weeks&rollingAverage=8hours&format=json

# volume comparesio
# median-confirmation-time
# transaction-fees
# cost-per-transaction-percent
# n-unique-addresses
# n-transactions-excluding-popular
# n-transactions-excluding-chains-longer-than-100
create_logger()
t_bitcoin_markets = tb.TickerBase(60.0 * 15, 'https://poloniex.com/public?command=returnTicker', 'localhost', 'markets')
_thread.start_new_thread(t_bitcoin_markets.run, ())

t_bitcoin_fees = tb.TickerBase(60.0, 'https://bitcoinfees.21.co/api/v1/fees/recommended',
                               'localhost', 'bitcoin_fees')
_thread.start_new_thread(t_bitcoin_fees.run, ())

# list all currencies: https://poloniex.com/public?command=returnCurrencies
t_exchange_rates = tb.TickerBase(60.0, 'https://poloniex.com/public?command=returnTicker', 'localhost', 'poloniex')
_thread.start_new_thread(t_exchange_rates.run, ())

t_crypto_coin_market = tb.TickerBase(60.0, 'https://api.coinmarketcap.com/v1/ticker/?limit=100',
                                     'localhost', 'crypto_coin_market')
_thread.start_new_thread(t_crypto_coin_market.run, ())

t_coin_marketcap_global = tb.TickerBase(60.0, 'https://api.coinmarketcap.com/v1/global/', 'localhost',
                                        'crypto_coin_global')
_thread.start_new_thread(t_coin_marketcap_global.run, ())
while 1:
    pass
