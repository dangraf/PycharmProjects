import abc
import pandas as pd

class myBase(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def apa(self, p):
        print 'apa'


df =  pd.DataFrame(columns=['a','b'], data = [[0.0, 0.1]] )

print df

index = df.__len__()

print index
df.loc[index] = [0.1,0.2]
print df
