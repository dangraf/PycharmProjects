""" author: Daniel Grafström
    file for converting imported data to dataframes"""

import numpy as np
import pandas as pd
import datetime as dt
import time
from pyvalid import accepts, returns


@accepts(int)
def _timestamp_to_datetime(timestamp):
    ret = dt.datetime.fromtimestamp(int(timestamp))
    return ret


@accepts(str)
def _datetime_to_timestamp(my_date_string):
    d_time = dt.datetime.strptime(my_date_string, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(d_time.timetuple()))


@accepts(pd.DataFrame, (str, int, None), (str, int, None))
def _slice_df_by_date(df_in, date_start, date_end):

    df_out = df_in.copy()
    # converts data to correct format
    if type(date_start) == str:
        date_start = _datetime_to_timestamp(date_start)

    if type(date_end) == int:
        date_end = _datetime_to_timestamp(date_end)
    # filter data depending on timestamp
    if date_start is not None:
        df_out = df_in.where(df_out['timestamp'] > date_start)

    if date_end is not None:
        df_out = df_out.where(df_out['timestamp'] < date_end)

    df_out.dropna(inplace=True)
    return df_out


@accepts(pd.DataFrame, any, bool)
@returns(pd.DataFrame)
def normalize_dataframe(dataframe,scaler, inverce=False ):
    """
    Normalizes all columns in a dataframe using scikit-learn scaler
    :param dataframe: dataframe containing data
    :param scaler:  scikit-learn scaler
    :param inverce: if True, it converts back to original values
    :return: dataframe
    """
    columns = dataframe.columns
    if inverce:
        for col in columns:
            dataframe[col] = scaler.inverse_transform(dataframe[col].values.reshape(-1, 1))
    else:
        for col in columns:
            dataframe[col] = scaler.fit_transform(dataframe[col].values.reshape(-1, 1))

    return dataframe

@returns(pd.DataFrame)
@accepts(str, str, (int, str), (int, str))
def get_dataframe_from_historicaldata(filename, groupinterval='1min', time_start=None, time_end=None):
    """Return a cleanded pandas dataframe
    Keyword arguments:
        filename -- filename of CSV file to be converted
        groupIntervalS -- eg '30s' or '1min' or similar (default 1min
        timeStart -- unix timestamp or string on format '2011-09-13 15:53:44' (default none)
        timeEnd -- unix timestamp or string on format '2011-09-13 15:53:44' (default none)
        """
    df = pd.read_csv(filename)
    df.columns = ['timestamp', 'price', 'volume']

    df = _slice_df_by_date(df, time_start, time_end)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df.set_index('datetime')
    df = df.groupby(pd.TimeGrouper(groupinterval)).agg({'price': np.mean, 'volume': np.sum})
    df['price'].ffill(inplace=True)
    df['volume'].fillna(0, inplace=True)

    return df

@returns(np.ndarray)
@accepts((pd.DataFrame, np.ndarray), int)
def split_sequential_df_to_matrix(dataframe, sequence_len):
    """
    Takes a dataframe containing sequential data and splits it up into smaller pieces.
    eg dataframe [1,2 3 4,5 6] sequence_len = 3
    return will be
    [1,2,3
    2,3,4
    3,4,5
    4,5,6]

    :param dataframe: pandas dataframe or numpy matrix to split
    :param sequence_len: lenght of sequence
    :return:
    """
    l = len(dataframe)
    if type(dataframe) == pd.DataFrame:
        data = dataframe.as_matrix()
    else:
        data = dataframe

    result = []
    for i in range(l-sequence_len+1):
        result.append(data[i:i+sequence_len])
    ret = np.array(result)
    return ret




