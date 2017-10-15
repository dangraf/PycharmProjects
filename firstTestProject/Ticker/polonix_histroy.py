import os
import time
import pandas as pd
import datetime
from dateutil import parser
import numpy as np
import pymongo


FETCH_URL = "https://poloniex.com/public?command=returnTradeHistory&currencyPair=%s&start=%d&end=%d"
# FETCH_URL = "https://poloniex.com/public?command=returnChartData&currencyPair=%s&start=%d&end=%d&period=300"
# PAIR_LIST = ["BTC_ETH"]


client = pymongo.MongoClient('localhost',)
DB = client.polonix


def compress_data(df):
    """ groups data into 1min intervals
        returns dataframe
    """
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(['date', 'type'], inplace=True)
    df2 = df.groupby([pd.TimeGrouper('1min', level='date'), pd.Grouper(level='type')]).agg(
        {'rate': np.mean, 'amount': np.sum, 'total': np.sum}, inplace=True)
    df2.reset_index(inplace=True)
    return df2


def get_latest_date(collection_name):
    """ looks into database to find latest record"""
    try:
        cursor = DB[collection_name].find({"$query": {}, "$orderby": {'date': -1}}).limit(1)
        date = cursor[0]['date']
    except BaseException as e:
        print(e)
        date = None
    return date


def save_to_mongodb(df, collection_name):
    """ saves data """
    collection = DB[collection_name]
    collection.insert_many(df.to_dict('records'))


def get_data(pair):
    """
    gets all data for the crypto-pair
    :param pair:
    :return:
    """

    date = get_latest_date(pair)
    if date is None:
        dt_start = datetime.datetime(2017, 1, 1)
    else:
        dt_start = date

    while 1:
        temp_end = dt_start + datetime.timedelta(days=30)
        url = FETCH_URL % (pair, dt_start.timestamp(), temp_end.timestamp())
        print("Get %s from %s to %s" % (pair, dt_start, temp_end))
        dt_start = temp_end

        print(dt_start)
        df = pd.read_json(url, convert_dates=False)
        if len(df) == 0:
            print("No data.")
            dt_start = temp_end
        else:
            df2 = compress_data(df)
            save_to_mongodb(df2, pair)

            dt_start = parser.parse(df['date'].iloc[-1])
            dt_gmt_now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            logend = (dt_start + datetime.timedelta(minutes=2)).replace(tzinfo=None)
            if logend > dt_gmt_now:
                # we have reached the end of the data.
                break

        time.sleep(30)
    print("Finish.")


def main():

    df = pd.read_json("https://poloniex.com/public?command=return24hVolume")
    pairs = [pair for pair in df.columns if pair.startswith('BTC')]
    print(pairs)

    for pair in pairs:
        get_data(pair)
        time.sleep(2)

if __name__ == '__main__':
    main()