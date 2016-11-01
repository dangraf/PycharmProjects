import numpy as np
import pandas as pd
import json

def subinterpolate( stepInSec,timestamp,price,volume ):

    outputTimestamp = []
    outputBid = []
    outputAmount = []
    #expand/collaps array to 1sec ticks
    for i in range(len(timestamp)-1):
        tm = range(timestamp[i],timestamp[i+1],1)
        if(len(tm)>1):
            outputTimestamp.extend(tm)
            temp = np.empty(len(tm))
            temp.fill(price[i])
            outputBid.extend(temp)
            temp.fill(0)
            temp[0] = volume[i]
            outputAmount.extend(temp)
    #fill up array to be equally divided into stepInSec, chunks
    mod = len(outputTimestamp)%stepInSec
    fill = stepInSec - mod

    tm = range(timestamp[-1],timestamp[-1]+fill,1)
    outputTimestamp.extend(tm)
    temp = np.empty(len(tm))
    temp[0] = price[-1]
    outputBid.extend(temp)
    temp[0] = volume[-1]
    outputAmount.extend(temp)
    # create New shapes
    rsAmount = np.reshape(outputAmount,(-1,stepInSec))
    rsTime = np.reshape(outputTimestamp,(-1,stepInSec))
    rsBid = np.reshape(outputBid,(-1,stepInSec))

    ouputLen = len(outputTimestamp)/stepInSec
#    rsBid = np.reshape(price,(stepInSec,-1))

    outputTm = rsTime[:,fill-1]

    outputAm = np.zeros(ouputLen)
    outputBid =np.zeros(ouputLen)

    for i in range(stepInSec):
        outputBid += rsBid[:,i]*rsAmount[:,i]
        outputAm += rsAmount[:,i]


    for i in range(ouputLen):
        if(outputAm[i] <0.00001):
            outputBid[i] = outputBid[i-1]
        else:
            outputBid[i] = outputBid[i]/outputAm[i]

    return [outputTm, outputBid, outputAm]


def readCsv( filePath, timeStepInSec  ):
    f = open( filePath,'r')
    d = f.readlines()
    f.close()

    time = []
    last =[]
    volume = []
#temp = []



    for row in d[1:]:

            v = row.split(',')[2] #volume
            r = row.split(',')[1] #last
            t = row.split(',')[0] #time

            last.append( float(r) )
            volume.append( float(v))
            time.append( int(float(t)))
#           endIndex = offset+chunkSize

    return subinterpolate( timeStepInSec,time,last,volume )

def getFutureFiltered( dataFrame,myFilter ):

    filtchange = np.convolve(dataFrame['price'],myFilter,'valid')
#    price = np.array(price[:-(len(myFilter)-1)])

    filtchange = np.divide(filtchange,dataFrame['price'][:-len(myFilter)+1]) - 1.0
    myindex = dataFrame.index
    myindex = myindex[:-len(myFilter)+1]

    dataFrame['FutureFilter'] = pd.Series(filtchange,index = myindex)

#    volume = np.array(volume[:-(len(myFilter)-1)])
#    dates = np.array(dates[:-(len(myFilter)-1)])
    return dataFrame

def getHistoryFiltered( dataFrame,myFilter ):

    filtchange = np.convolve(dataFrame['price'],myFilter,'valid')
    print dataFrame['price'][len(myFilter)-1:]
    filtchange = np.divide(filtchange,dataFrame['price'][len(myFilter)-1:])-1


#    myindex = dataFrame.index
#    myindex = myindex[-len(myFilter)-1:]

    #dataFrame['HistoryFilter'] = pd.Series(filtchange,index = myindex)
    dataFrame['HistoryFilter'] = filtchange
    return dataFrame

def getFutureFilter( indexArray):
    myFilter = np.zeros(np.max(indexArray)+1)
    for index in indexArray:
        myFilter[index-1] = 1.0/len(indexArray)
    return myFilter

def getHistoryFilter( indexArray ):
    myFilter = np.zeros(np.max(indexArray)+1)
    for index in indexArray:
        myFilter[index] = 1.0/len(indexArray)

    return myFilter

# Calculates orderdepth rato
# todo,handle price information together with volume information.x
def getOrderDepthRatio( filename, topNumOrders ):
    """ testing To get some Infor from it """
    indexVolume = 1

    f = open(filename,'r')
    d = f.readlines()
    f.close();

    output = []

    for r in d:

        data = json.loads(r)
        bidsvolume = np.array(data['bids'][0:topNumOrders]).astype(float)
        asksvolume = np.array(data['asks'][0:topNumOrders]).astype(float)
        timestamp= np.int64(data['date'])
#        if( len(output)>1 and  timestamp < output[-1][0]):
#                print timestamp

        sumBid = sum(bidsvolume[:,indexVolume])
        sumAsk = sum(asksvolume[:,indexVolume])
        ratio = (sumBid-sumAsk)/(sumBid+sumAsk)
        output.append([timestamp,ratio])

    out = np.array(output)

#    ratioSeries = pd.Series(out[:,1],index=np.transpose( np.int64(out[:,0])),name='od_ratio' )
    ratioSeries = pd.DataFrame([out[:,0],out[:,1]]).T

    ratioSeries.columns= ['date','od_ratio']
    ratioSeries['date'] = ratioSeries['date'].astype(np.int64)
#    ratioSeries.index.name = 'date'

    ratioSeries = ratioSeries.groupby('date').mean()

    #ratioArray = pd.DataFrame(out[:,1],index=np.int64(out[:,0]))

    return ratioSeries

# Reads csv Chart using price,  date and volume (no orderdepth)
# groups volumes into 1sek data. Some dates may be missing when no trading occures.
def readCsvChart(filenamePrice):
    tmpPrice = pd.read_csv(filenamePrice)
    tmpPrice.columns = ['date','price','volume']
    priceGr = tmpPrice.groupby('date')
    price = priceGr.agg({'price':np.mean,'volume':np.sum})


    return price
#private function,  used to fill create a complete array of price,  volume anad orderdepth
# with 1sek data
def fillAndSetData(dataframe,timestampStart=None,timestampEnd=None):
    #hitta start och slut index
    #skapa en index-lista for samtilga instanser
    #lagga ihop bada arrayerna.

    if( timestampStart != None):
        newIndex = range(timestampStart,timestampEnd)
        dataframe = pd.DataFrame(dataframe,index = newIndex )

    if 'price' in dataframe.columns:
        dataframe['price'] = dataframe['price'].ffill()
    if 'od_ratio' in dataframe.columns:
        dataframe['od_ratio'] = dataframe['od_ratio'].ffill()
    if 'volume' in dataframe.columns:
        dataframe['volume'] = dataframe['volume'].fillna(0)



    return dataframe

# takes two files with
def syncPriceAndOrderdepth(timestampStart,timestampEnd,filenamePrice,filenameOrdDepth):

    priceData = readCsvChart( filenamePrice )
    S_price = pd.Series(priceData['price'])
    S_volume = pd.Series(priceData['volume'])

    ratio = getOrderDepthRatio(filenameOrdDepth,20)

    S_ratio = pd.Series(ratio['od_ratio'])

#    S_ratio.to_csv('od_ratio.csv')

    combinedData = pd.DataFrame([S_price,S_volume,S_ratio]).T
    combinedData.index.name = 'date'


    out = fillAndSetData(combinedData,timestampStart,timestampEnd )


    #print out
    return out




