# -*- coding: utf-8 -*-
"""
Base class for fetching data from a home-page and save it to a mongo-db

_author__ =  "Daniel Grafström"
__license__ = "GPL"
__status__ = "Experimental"
"""

import datetime as dt
from time import sleep
import urllib.request as urlreq
import urllib.error as urlerr
import json
from pymongo import MongoClient
from pymongo import errors
import datetime
import logging


class TickerBase:
    """ baseclass handeling """
    def __init__(self, update_period_s, url, mongodb_url, db_collection_name):

        self.UpdatePeriodS = update_period_s
        self.url = url
        self.LastUpdate = dt.datetime.fromtimestamp(0)
        self.iterator = 0
        self.running = True
        self.data = []
        self.mongodb_url = mongodb_url
        self.db_collection_name = db_collection_name
        self.db_col = None
        self.db_client = None
        self.logger = None

        self.get_logger()

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
        logger_name = 'main_scraper.' + self.db_collection_name
        self.logger = logging.getLogger(logger_name)
        self.logger.info("started logging for{0}".format(logger_name))

    def wait_until_next_update(self):
        """whait until next update
        """
        current_time = dt.datetime.now()

        time_to_wait = self.UpdatePeriodS - (current_time - self.LastUpdate).total_seconds()
        logging.info(time_to_wait)
        if time_to_wait < 0:
            time_to_wait = self.UpdatePeriodS
        sleep(time_to_wait)
        self.LastUpdate = dt.datetime.now()

    def get_data_save_to_db(self):
        """Reads data from url and saves it to database"""

        req = urlreq.Request(url=self.url, headers={'User-Agent': "Magic Browser"})

        try:
            response = urlreq.urlopen(req)
        except urlerr.HTTPError as e:
            self.logger.error('Server could not fulfill request: {0} errorcode: {1}'.format(self.url, e.code))
        except urlerr.URLError as e:
            self.logger.error('failed to reach a server: {0} errorcode: {1}'.format(self.url, e.reason))
        else:
            the_page = response.read()
            encoding = response.info().get_content_charset('utf-8')

            data = json.loads(the_page.decode(encoding))
            self.logger.info('Received {0} chunk of data'.format(len(data)))
            if len(data) == 0:
                self.logger.info('Received data with length 0')
            else:
                try:
                    self.connect_db()
                    doc = {'timestamp': datetime.datetime.utcnow(),
                           'data': data}
                    self.db_col.insert_one(doc)
                    self.db_client.close()
                except errors.ConnectionFailure:
                    self.logger.error('Lost connection to mongo-db')
                except errors.ExecutionTimeout:
                    self.logger.error('mongo-db timeot')


        # Todo, handle re-connection when it's lost
        # Todo, check length of data to prevent empty frames

    def run(self):
        while self.running:
            self.get_data_save_to_db()
            self.wait_until_next_update()





