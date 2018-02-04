from Projects.mongo_data.settings_data import SettingsList, get_safe_settingslist
from Projects.mongo_data.crypto_news_data import CryptoNews
import newspaper
import logging

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


def get_news_data():
    # Get list of settings
    urllist: SettingsList = get_safe_settingslist('CryptoNewsUrls', urls)
    keylist: SettingsList = get_safe_settingslist('CrytoNewsKeywords', keywords)

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
                    obj = CryptoNews.objects(title=article.title).first()
                    if obj is None:
                        news = CryptoNews()
                        news.title = article.title
                        news.description = article.meta_description
                        news.text = article.text[0:200]
                        news.tags = keys
                        news.url = article.url
                        news.save()
                        logger.info(article.title)

            except BaseException as e:
                logger.error('Cryptonews error{0}'.format(e))
                pass
