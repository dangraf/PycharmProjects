from bs4 import BeautifulSoup
import requests
from datetime import datetime
from datetime import timedelta
import logging
from pymongo import MongoClient
from pymongo import errors


class ParseBitcoinNews:
    """ reads bitcoin news and saves to mongodb needs to be called from mainscraper"""
    def __init__(self):
        self.url = 'https://news.bitcoin.com/'
        self.histData = []
        self.logger = None
        self.get_logger()
        self.db_collection_name = 'btc_news'
        self.db_client = None
        self.db_col = None
        self.mongodb_url = 'localhost'

    def connect_db(self):
        """ tries to connect to mongodb"""
        if self.mongodb_url is None or self.db_collection_name is None:
            return
        try:
            self.db_client = MongoClient(self.mongodb_url, 27017)
            db = self.db_client['ticker_db']
            self.db_col = db[self.db_collection_name]

        except errors.ConnectionFailure as e:
            self.logger.error('unable to connect to mongodb: {0}'.format(e))

    def get_logger(self):
        """ gets logger defined in main_scraper"""
        logger_name = 'main_scraper.' + "bitcoin_news"
        self.logger = logging.getLogger(logger_name)
        self.logger.info("started logging for{0}".format(logger_name))

    def check_for_news(self):
        """ connects to bitcoin news url and saves new headlines to db"""
        r = requests.get(self.url)
        data = r.text
        soup = BeautifulSoup(data, "lxml")

        for link in soup.findAll("div", {"class": "td-big-grid-meta"}):
            data = {'text': link.find_all('a')[0].text, 'time': datetime.now()}
            self.connect_db()
            if self.db_col.find_one({'text': data['text']}) is not None:
                self.db_col.insert_one(data)
                self.logger.info('adding data: {0}, {1}'.format(data['time'], data['text']))
            self.db_client.close()

