from datetime import datetime
from mongoengine import DynamicDocument, DateTimeField, Document, StringField
from typing import List

class TickerDataSettings(Document):
    url = StringField(required=True, unique=True)
    collectionName = StringField(required=True, unique=True)
    meta = {'db_alias': 'settings',
            'collection': 'ticker_settings'}

def get_TickerSettings(default_list)->List[TickerDataSettings]:
    mylist = TickerDataSettings.objects()
    if mylist is None:
        settings = TickerDataSettings()
        for obj in default_list:
            settings.url = obj['url']
            settings.collectionName = obj['name']
            settings.save()
        mylist = TickerDataSettings.objects()

    return List(mylist)
class TickerData(DynamicDocument):
    timestamp = DateTimeField(default=datetime.now, unique=True)
    meta = {
        'db_alias': 'ticker',
        'collection': 'CryptoNews'
    }


def save_tickerdata(data, collectionName: str):
    try:
        obj = TickerData()
        obj.data = data
        obj.switch_collection(collectionName)
        obj.save()
    except BaseException as e:
        print(e)

