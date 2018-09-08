from Ticker.datahelpers import GetUrlData, get_new_unique_data
import Ticker.mongo_obj as mongo
import pandas as pd
from Projects.mongo_data.settings_data import SettingsList, get_safe_settingslist

import newspaper
import logging
import requests

#df_prev = None


def get_coinmarketcap():
    #global df_prev

    getter = GetUrlData('https://api.coinmarketcap.com/v1/ticker/?limit=100')
    getter.do_work()
    df = None
    try:
        data = getter.get_result()
        df = pd.DataFrame(data)

        #dfs = get_new_unique_data(old_df=df_prev, new_df=df)
        mongo.save_tickerdata(data=df.to_dict(orient='records'), collection_name="coinmarketcap_top100")
        #df_prev = df
    except BaseException as e:
        if df is None:
            # this is a get-data error
            raise BaseException(e + 'When getting coinmarketcap data')
        else:
            # this is either a parsing error or save to database error.
            raise type(e)(e.message + 'When parsing and saving data')

def get_fear_greed_index():
        try:
            r = requests.get("https://money.cnn.com/data/fear-and-greed/")
            data = r.text
            search_str = "Greed Now:"
            start = data.find("Greed Now:") + len(search_str)
            substr = data[start:start + 10]
            end = substr.find('(')
            greed_index = int(substr[:end].strip())
            mongo.save_tickerdata(data=greed_index, collection_name='fear_and_greed_index')
        except BaseException as e:
            raise BaseException(e + "when getting fear_greed index")

def get_global_cap():
    getter = GetUrlData('https://api.coinmarketcap.com/v1/global/')
    getter.do_work()
    try:
        data = getter.get_result()
        mongo.save_tickerdata(data=data, collection_name='global_market')
    except BaseException as e:
        raise BaseException(e + 'When getting global_market data')

df_bitcoincharts = None
# max every 15 minutes
def get_bitcoincharts_data():
    global df_bitcoincharts
    getter = GetUrlData('http://api.bitcoincharts.com/v1/markets.json')
    getter.do_work()
    try:
        data = getter.get_result()
        df = pd.DataFrame(data)
        df2 = get_new_unique_data(old_df= df_bitcoincharts, new_df=df)
        mongo.save_tickerdata(data=df2.to_dict(orient='records'), collection_name='bitcoincharts_global')
        df_bitcoincharts = df
    except BaseException as e:
        raise BaseException(e+" when getting bitcoincharts data")

# def get_bitcoinaverage_ticker_data():
#    getter = GetUrlData('https://apiv2.bitcoinaverage.com/indices/global/ticker/short?crypto=BTC,BTH,LTC,XRP,ETH,ETC,USDT,DASH,EOS,XLM&fiat=USD')
#    getter.do_work()
#    try:
#        data= getter.get_result()
#        df = pd.DataFrame(data).T.reset_index()
#        df.rename(columns={'index': 'pair'}, inplace=True)
#        mongo.save_tickerdata(data=df.to_dict(orient='records'), collection_name='bitcoinaverage_ticker')
#    except BaseException as e:
#        raise BaseException(e + 'When getting bitcoinaverage ticker data')

def get_bitcoin_fees():
    getter = GetUrlData('https://bitcoinfees.21.co/api/v1/fees/recommended')
    getter.do_work()
    try:
        data = getter.get_result()
        mongo.save_tickerdata(data=data, collection_name='bitcoin_fees')
    except BaseException as e:
        raise BaseException(e + 'When getting bitcoin fees')



urls = ['https://techcrunch.com/',
        'https://www.nbcnews.com/',
        'https://www.cnbc.com/',
        'https://www.marketwatch.com/',
        'http://fortune.com/',
        'https://www.forbes.com/',
        'https://cointelegraph.com/',
        'https://www.coindesk.com/',
        'https://www.theguardian.com/'
        'https://www.ft.com/',
        'http://www.bbc.com/',
        'http://time.com/',
        'https://www.pri.org',
        'http://www.businessinsider.com',
        'https://arstechnica.com',
        'https://www.investopedia.com',
        'https://www.washingtonpost.com',
        'https://www.wired.com']


keywords = ['bitcoin', 'ripple', 'ethereum', 'litecoin',
            'dash', ' eos ', ' neo ', 'stellar', ' nem ', 'Tether']

# get every 30 minutes? 15 seems too fast sometimes
def get_news_data():
    # Get list of settings
    try:
        urllist: SettingsList = get_safe_settingslist('CryptoNewsUrls', urls)
        keylist: SettingsList = get_safe_settingslist('CrytoNewsKeywords', keywords)
    except BaseException as e:
        raise BaseException(e + "When getting settings lists for bitcoin news")

    logger_name = 'main_scraper.' + "bitcoin_news"
    logger = logging.getLogger(logger_name)

    for url in urllist.list:
        paper = newspaper.build(url, language='en')
        for article in paper.articles:
            try:
                article.download()
                article.parse()

                keys = [key for key in keylist.list if key in article.title.lower()]
                if len(keys) > 0:
                    # check if article already exists
                    obj = mongo.CryptoNews.objects(title=article.title).first()
                    if obj is None:
                        news = mongo.CryptoNews()
                        news.title = article.title
                        news.description = article.meta_description
                        news.text = article.text
                        news.tags = keys
                        news.url = article.url
                        a = article.nlp()       # how to handle updates, save first then do npl?
                        news.time_posted = article.publish_date
                        news.summary = article.summary
                        news.keywords = article.keywords

                        news.save()
                        logger.info(article.title)

                        # article.keywords
                        # article.summary
                        # article.publish_date
                        # source_url

            except BaseException as e:
                logger.error('Cryptonews error{0}'.format(e))
                pass