from mongoengine import Document, DateTimeField, StringField, ListField
from datetime import datetime


class CryptoNews(Document):
    timestamp = DateTimeField(default=datetime.now)
    tags = ListField(StringField(), required=True)
    title = StringField(max_length=200, required=True, unique=True)
    description = StringField(max_length=200, required=True)
    text = StringField(max_length=200, required=True)
    url = StringField(max_length=200, required=True)
    meta = {
        'db_alias': 'NewsDb',
        'collection': 'CryptoNews'
    }
