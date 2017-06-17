import datetime as dt
from time import sleep
import urllib.request as urlreq
import urllib.error as urlerr
import json
from pandas.io.json import json_normalize
import pandas as pd
import pickle


class ticker_base:
    def __init__(self, filenamePath, updatePeriodS, url):
        self.filename = filenamePath
        self.UpdatePeriodS = updatePeriodS
        self.url = url
        self.LastUpdate = dt.datetime.fromtimestamp(0)
        self.iterator = 0
        self.running = True
        self.data = []



    def waitUntilNextUpdate(self):
        #whait until next update
        current_time = dt.datetime.now()

        time_to_wait = self.UpdatePeriodS- (current_time - self.LastUpdate).total_seconds()
        print(time_to_wait)
        if  time_to_wait<0:
            time_to_wait = self.UpdatePeriodS
        sleep(time_to_wait)
        self.LastUpdate = dt.datetime.now()

    def getData(self):
        df_ = pd.DataFrame()
        df = df_.fillna(0)  # with 0s rather than NaNs
        req = urlreq.Request(url=self.url, headers={'User-Agent' : "Magic Browser"})

        try:
            response = urlreq.urlopen(req)

        except urlerr.HTTPError as e:
            print('error on url:',self.url)
            print( 'The server couldn\'t fulfill the request.')
            print ('Error code: ', e.code)
        except urlerr.URLError as e:
            print('error on url:', self.url)
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
            the_page = response.read()
            encoding = response.info().get_content_charset('utf-8')
            try:
                data = json.loads(the_page.decode(encoding))
                df = json_normalize(data)
            except:
                print('unable to parse data from homepage to pandas')


        return df
    def run(self):
        while self.running:
            try:
                allData = pd.read_pickle(self.filename)
            except:
                print('unable to load file')
                allData = []

            df = self.getData()
            if( len(allData) == 0):
                allData = df
            else:
                allData = allData.append(df)
            allData.to_pickle(self.filename)


            self.iterator +=1
            print(allData.shape)
             #clear memory
            temp = [allData]
            del temp
            self.waitUntilNextUpdate()





