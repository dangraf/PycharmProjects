from datetime import datetime
from mongoengine import DynamicDocument, DateTimeField, Document, StringField
from typing import List

default_list = [{'url':'https://bitcoinfees.21.co/api/v1/fees/recommended', 'name':'bitcoin_fees'},
                {'url':'https://poloniex.com/public?command=returnTicker', 'name':'markets'},
                {'url':'https://api.coinmarketcap.com/v1/ticker/?limit=100','name':'crypto_coin_market'},
                {'url':'https://api.coinmarketcap.com/v1/global/','name':'crypto_coin_global'}]


class TickerDataSettings(Document):
    url = StringField(required=True, unique=True)
    collectionName = StringField(required=True, unique=True)
    meta = {'db_alias': 'settings',
            'collection': 'ticker_settings'}

def get_TickerSettings()->List[TickerDataSettings]:
    mylist = TickerDataSettings.objects()
    if len(mylist) == 0:
        settings = TickerDataSettings()
        for obj in default_list:
            settings = TickerDataSettings()
            settings.url = obj['url']
            settings.collectionName = obj['name']
            settings.save()
        mylist = TickerDataSettings.objects()
    return list(mylist)

class TickerData(DynamicDocument):
    timestamp = DateTimeField(default=datetime.now, unique=True)
    meta = {
        'db_alias': 'ticker',
        'collection': 'Uninitiated'
    }


def save_tickerdata(data, collectionName: str):
    try:
        obj = TickerData()
        obj.data = data
        obj.switch_collection(collectionName)
        obj.save()
    except BaseException as e:
        print(e)

