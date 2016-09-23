import json
class argbase():
    filename = 'argDump.txt'
    dict = {'treshold':{'max':1.0,'min':0.0,'v':0.2}}

    def load(self):
        fp = open(self.filename, 'r')

        self.dict = json.load( fp )
        fp.close()


    def save(self):
        fp = open(self.filename, 'wb')
        a = json.dumps(self.dict, default=lambda obj: obj.__dict__)
        fp.write(a)
        fp.close()

