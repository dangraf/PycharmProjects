from mongoengine import DynamicDocument, DateTimeField, Document, StringField, ListField
from datetime import datetime
import mongoengine


class TickerData(DynamicDocument):
    timestamp = DateTimeField(default=datetime.now, unique=True)
    meta = {
        'db_alias': 'ticker',
        'collection': 'Uninitiated'
    }


class CryptoNews(Document):
    timestamp = DateTimeField(default=datetime.now)
    tags = ListField(StringField(), required=True)
    title = StringField(max_length=200, required=True, unique=True)
    description = StringField(max_length=200, required=True)
    text = StringField(required=True)
    url = StringField(max_length=200, required=True)
    time_posted = DateTimeField(required=False)
    summay = StringField(required=False)
    keywords = ListField(StringField(), required=False)
    meta = {
        'db_alias': 'NewsDb',
        'collection': 'CryptoNews'
    }


def init_mongodb():
    mongoengine.register_connection(alias='settings', name='apps_settings', host='userver', port=27017)
    mongoengine.register_connection(alias='NewsDb', name='ticker3_db', host='userver', port=27017)
    mongoengine.register_connection(alias='ticker', name='ticker3_db', host='userver', port=27017)


def save_tickerdata(*, data, collection_name: str):
    try:
        obj = TickerData()
        obj.data = data
        obj.switch_collection(collection_name)
        obj.save()
    except BaseException as e:
        print(e)
