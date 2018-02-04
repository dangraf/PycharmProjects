# -*- coding: utf-8 -*-
"""
Main app for fetching data from a home-page and save it to a mongo-db

_author__ =  "Daniel Grafström"
__license__ = "GPL"
__status__ = "Experimental"
"""

import logging
import schedule # https://pypi.python.org/pypi/schedule
from Projects.mongo_data.mongo_init import init_mongodb
from Projects.Scraper.cryptonews_scraper import get_news_data
from Projects.Scraper.crypto_ticker import get_ticker_data
from time import sleep


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


init_mongodb()
create_logger()
schedule.every(15).minutes.do(get_news_data)
schedule.every().minute.do(get_ticker_data)
while 1:
    schedule.run_pending()
    sleep(5)
