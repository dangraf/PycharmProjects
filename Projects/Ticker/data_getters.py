from datahelpers import GetUrlData
import mongo_obj as mongo
import pandas as pd
# from  Projects.mongo_data.settings_data import SettingsList, get_safe_settingslist
import krakenex
import newspaper
import logging
import requests


# df_prev = None


def get_coinmarketcap():
    # global df_prev

    getter = GetUrlData('https://api.coinmarketcap.com/v1/ticker/?limit=100')
    getter.do_work()

    try:
        data = getter.get_result()
        df = pd.DataFrame(data)

        # dfs = get_new_unique_data(old_df=df_prev, new_df=df)
        mongo.save_tickerdata(data=df.to_dict(orient='records'), collection_name="coinmarketcap_top100")
        # df_prev = df
    except BaseException as e:
        raise BaseException(f'{e}: When getting coinmarketcap data')


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
        raise BaseException(f"{e} when getting fear_greed index")


def get_kraken_orderdepth():
    retries = 3
    depth = '20'
    kraken = krakenex.API()
    # https://api.kraken.com/0/public/AssetPairs
    pairs = ['EOSUSD', 'BCHUSD', 'XXLMZUSD',
             'XXMRZUSD',
             'XXRPZUSD',
             'XETHZUSD',
             'XLTCZUSD',
             'XETCZUSD']
    for pair in pairs:
        for i in range(retries):
            try:
                response = kraken.query_public('Depth', {'pair': pair, 'count': depth})
                df1 = pd.DataFrame(response['result'][pair]['asks'], columns=['price', 'volume', 'timestamp'])
                df2 = pd.DataFrame(response['result'][pair]['bids'], columns=['price', 'volume', 'timestamp'])
                # restructure data for better searchability
                data = {'bids': df2.to_dict(orient='list'),
                        'asks': df1.to_dict(orient='list'),
                        'pair': pair}
                mongo.save_tickerdata(data=data, collection_name='kraken_orderdepth')
                break
            except BaseException as e:
                raise BaseException(f"{e} when getting fear_greed index")


def get_global_cap():
    getter = GetUrlData('https://api.coinmarketcap.com/v1/global/')
    getter.do_work()
    try:
        data = getter.get_result()
        mongo.save_tickerdata(data=data, collection_name='global_market')
    except BaseException as e:
        raise BaseException(f"{e}: When getting global_market data")


df_bitcoincharts = None


# max every 15 minutes
def get_bitcoincharts_data():
    global df_bitcoincharts
    getter = GetUrlData('http://api.bitcoincharts.com/v1/markets.json')
    getter.do_work()
    try:
        data = getter.get_result()
        df = pd.DataFrame(data)
        # df2 = get_new_unique_data(old_df=df_bitcoincharts, new_df=df)
        mongo.save_tickerdata(data=df.to_dict(orient='records'), collection_name='bitcoincharts_global')
        df_bitcoincharts = df
    except BaseException as e:
        raise BaseException(f"{e}:  when getting bitcoincharts data")


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
        raise BaseException(f"{e}: When getting bitcoin fees")


# get every 30 minutes? 15 seems too fast sometimes
def get_news_data():
    # Get list of settings
    try:
        urllist: mongo.SettingsList = mongo.get_settingslist('CryptoNewsUrls')
        keylist: mongo.SettingsList = mongo.get_settingslist('CrytoNewsKeywords')
    except BaseException as e:
        raise BaseException(f"{e}: When getting settings lists for bitcoin news")

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
                        article.nlp()  # how to handle updates, save first then do npl?
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
