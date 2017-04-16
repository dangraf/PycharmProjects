import datetime as dt
from time import sleep
import urllib2
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
        req = urllib2.Request(self.url,headers={'User-Agent' : "Magic Browser"})
        df_ = pd.DataFrame()
        df = df_.fillna(0)  # with 0s rather than NaNs

        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except urllib2.URLError as e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        else:
            the_page = response.read()
            try:
                data = json.loads(the_page)
                df = json_normalize(data)
            except:
                print('unable to parse data from homepage to pandas')


        return df
    def run(self):
        while self.running:
            try:
                self.data = pd.read_pickle(self.filename)
            except:
                print('unable to load file')
                self.data = []

            df = self.getData()
            if( len(self.data) == 0):
                self.data = df
            else:
                self.data = self.data.append(df)
            self.data.to_pickle(self.filename)

            #pickle.dump(self.data, open( self.filename, "wb" ))
            self.iterator +=1
            print(self.data.shape)

            self.waitUntilNextUpdate()





