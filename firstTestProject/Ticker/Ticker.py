## api input:
# create:
# filename - CSV fileformat from bitcoincharts
# StartDate - where to start the sampling
# Range - how big the dataset is

#event-handler, possible to add event hooks

# startTick. -> steps through all data and calls all events.
import pandas as pd
import numpy as np


class ticker:


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

