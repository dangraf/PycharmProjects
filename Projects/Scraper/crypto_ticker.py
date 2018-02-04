
import logging
import urllib.request as urlreq
import urllib.error as urlerr
import json
from Projects.mongo_data.ticker_data import save_tickerdata,
import datetime

default_list = [{'url':'https://bitcoinfees.21.co/api/v1/fees/recommended', 'name':'bitcoin_fees'},
                {'url':'https://poloniex.com/public?command=returnTicker', 'name':'markets'},
                {'url':'https://api.coinmarketcap.com/v1/ticker/?limit=100','name':'crypto_coin_market'},
                {'url':'https://api.coinmarketcap.com/v1/global/','name':'crypto_coin_global'}]




def getTickerData():
    print(len(default_list))
    # todo, get list of all sites from db
    for obj in default_list:
        logger_name = 'main_scraper.' + obj.name
        logger = logging.getLogger(logger_name)

        req = urlreq.Request(url=obj.url, headers={'User-Agent': "Magic Browser"})

        try:
            response = urlreq.urlopen(req)
        except urlerr.HTTPError as e:
            logger.error('Server could not fulfill request: {0} errorcode: {1}'.format(self.url, e.code))
        except urlerr.URLError as e:
            logger.error('failed to reach a server: {0} errorcode: {1}'.format(self.url, e.reason))
        else:
            the_page = response.read()
            encoding = response.info().get_content_charset('utf-8')

            data = json.loads(the_page.decode(encoding))
            logger.info('Received {0} chunk of data'.format(len(data)))
            if len(data) == 0:
                logger.info('Received data with length 0')
            else:
                save_tickerdata(obj['name'],data)


    # todo, iterate over the sites and fetch data
print(len(default_list))