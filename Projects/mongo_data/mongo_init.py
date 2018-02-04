import mongoengine

def init_mongodb():
    mongoengine.register_connection(alias='settings', name='apps_settings', host='userver', port=27017)
    mongoengine.register_connection(alias='NewsDb', name='ticker_db', host='userver', port=27017)
    mongoengine.register_connection(alias='ticker', name='ticker_db', host='userver', port=27017)
