from pymongo import MongoClient
import datetime
import mongoengine


client = MongoClient('localhost', 27017)
db = client.test


post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

class Owner(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    name = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)

    snake_ids = mongoengine.ListField()
    cage_ids = mongoengine.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'owners'
    }


def hello(name: str, age: int)->str:
        print(type(age))
        print('my name is{} and Im {} years old'.format(name, age))
        return 0

a = hello('daniel', '30')
print(type(a))
