## api input:
# create:
# filename - CSV fileformat from bitcoincharts
# StartDate - where to start the sampling
# Range - how big the dataset is

#event-handler, possible to add event hooks

# startTick. -> steps through all data and calls all events.
import pandas as pd
import numpy as np

class Event:
    def __init__(self):
        self.handlers = set()

    def handle(self, handler):
        self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def getHandlerCount(self):
        return len(self.handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount


class ticker:
    def __init__(self):
        #creates an event with timestamp, price and volume every xx seconds
        self.ReportNewTickData = Event()

    # Private function
    def __readCsvChart(self, filenamePrice):
        tmpPrice = pd.read_csv(filenamePrice)
        tmpPrice.columns = ['date', 'price', 'volume']

        priceGr = tmpPrice.groupby('date')
        price = priceGr.agg({'price': np.mean, 'volume': np.sum})
        return price

        return price
    def PrepareFile( self, filename ):
        self.Data = self.__readCsvChart( filename )

