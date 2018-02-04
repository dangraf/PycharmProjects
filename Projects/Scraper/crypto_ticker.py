import logging
import urllib.request as urlreq
import urllib.error as urlerr
import json
from Projects.mongo_data.ticker_data import save_tickerdata, get_TickerSettings


def get_ticker_data():
    default_list = get_TickerSettings()
    for obj in default_list:
        logger_name = 'main_scraper.' + obj.collectionName
        logger = logging.getLogger(logger_name)
        req = urlreq.Request(url=obj.url, headers={'User-Agent': "Magic Browser"})

        try:
            response = urlreq.urlopen(req)
        except urlerr.HTTPError as e:
            logger.error('Server could not fulfill request: {0} errorcode: {1}'.format(obj.url, e.code))
        except urlerr.URLError as e:
            logger.error('failed to reach a server: {0} errorcode: {1}'.format(obj.url, e.reason))
        else:
            the_page = response.read()
            encoding = response.info().get_content_charset('utf-8')

            data = json.loads(the_page.decode(encoding))
            logger.info('Received {0} chunk of data'.format(len(data)))
            if len(data) == 0:
                logger.info('Received data with length 0')
            else:
                save_tickerdata(data, obj.collectionName)
