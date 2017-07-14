import numpy as np
import pandas as pd
import datetime as dt
import time
from pyvalid import accepts, returns

# Calculates orderdepth rato
# todo,handle price information together with volume information.x
#def getOrderDepthRatio( filename, topNumOrders ):
#    """ testing To get some Infor from it """
#    indexVolume = 1

#    f = open(filename,'r')
#    d = f.readlines()
#    f.close();

#    output = []

#    for r in d:

#        data = json.loads(r)
#        bidsvolume = np.array(data['bids'][0:topNumOrders]).astype(float)
#        asksvolume = np.array(data['asks'][0:topNumOrders]).astype(float)
#        timestamp= np.int64(data['date'])
#        if( len(output)>1 and  timestamp < output[-1][0]):
#                print timestamp

#        sumBid = sum(bidsvolume[:,indexVolume])
#        sumAsk = sum(asksvolume[:,indexVolume])
#        ratio = (sumBid-sumAsk)/(sumBid+sumAsk)
#        output.append([timestamp,ratio])

#    out = np.array(output)

#    ratioSeries = pd.Series(out[:,1],index=np.transpose( np.int64(out[:,0])),name='od_ratio' )
#    ratioSeries = pd.DataFrame([out[:,0],out[:,1]]).T

#    ratioSeries.columns= ['date','od_ratio']
#    ratioSeries['date'] = ratioSeries['date'].astype(np.int64)
#    ratioSeries.index.name = 'date'

#    ratioSeries = ratioSeries.groupby('date').mean()

    #ratioArray = pd.DataFrame(out[:,1],index=np.int64(out[:,0]))

#    return ratioSeries


@accepts(int)
def _timestamp_to_datetime(timestamp):
    ret = dt.datetime.fromtimestamp(int(timestamp))
    return ret

@accepts(str)
def _datetime_to_timestamp(myDateString):
    d_time = dt.datetime.strptime(myDateString, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(d_time.timetuple()))

@accepts(pd.core.frame.DataFrame, (str,int,None),(str,int,None))
def _slice_df_by_date(df_in, date_start, date_end):

    df_out = df_in.copy()
    if type(date_start)== str:
        date_start = _datetime_to_timestamp(date_start)
    if type(date_end) == int:
        date_end = _datetime_to_timestamp(date_end)

    if date_start != None :
        df_out = df_in.where( df_out['timestamp']>date_start )
    if date_end != None:
        df_out = df_out.where(df_out['timestamp']<date_end )

    df_out.dropna(inplace=True)


@returns(pd.core.frame.DataFrame)
@accepts(str, str,(int,str),(int,str))
def getDataFrameFromHistoricalData(filename, groupInterval = '1min', timeStart=None,timeEnd=None ):
    """Return a cleanded pandas dataframe
    Keyword arguments:
        filename -- filename of CSV file to be converted
        groupIntervalS -- eg '30s' or '1min' or similar (default 1min
        timeStart -- unix timestamp or string on format '2011-09-13 15:53:44' (default none)
        timeEnd -- unix timestamp or string on format '2011-09-13 15:53:44' (default none)
        """
    df = pd.read_csv( filename )
    df.columns = ['timestamp', 'price', 'volume']

    df['datetime'] = pd.to_datetime(df['timestamp'],unit='s')
    df = df.set_index('datetime')
    df = df.groupby(pd.TimeGrouper( groupInterval) ).agg({'price':np.mean,'volume':np.sum})
    df['price'].ffill(inplace=True)
    df['volume'].fillna(0,inplace=True)

    return df



#def syncPriceAndOrderdepth(timestampStart,timestampEnd,filenamePrice,filenameOrdDepth):

#    priceData = readCsvChart( filenamePrice )
#    S_price = pd.Series(priceData['price'])
#    S_volume = pd.Series(priceData['volume'])

#    ratio = getOrderDepthRatio(filenameOrdDepth,20)

#    S_ratio = pd.Series(ratio['od_ratio'])

#    S_ratio.to_csv('od_ratio.csv')

#    combinedData = pd.DataFrame([S_price,S_volume,S_ratio]).T
#    combinedData.index.name = 'date'


#    out = fillAndSetData(combinedData,timestampStart,timestampEnd )


    #print out
#    return out




