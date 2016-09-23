
import json

class myParams():

    dict = {'apa':{'max':1,'min':0},'bepa':{'max':10,'min':2}}
    dict['apa']['vale'] = 0.5
    dict['cepa'] = {'max':5,'min':-5}

    def save(self,filename):
        fp = open(filename, 'wb')
        json.dump(dict,fp)
        fp.close()

    def load(self,filename):

        fp = open(filename, 'r')
        json.load(dict, fp)
        fp.close()


    for a in dict.iteritems():
        print a[1]['min']


    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

def  PrintParams(obj):

    for attr, value in obj:

        print(attr,'=',value)


p = myParams()
p.threshold = 0.10
PrintParams(p)








