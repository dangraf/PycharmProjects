from unittest import TestCase
import argBase as ab
import os.path

__author__ = 'Daniel Grafstrom'
__project__ = 'InterfaceToExchange'

class test_argBase(TestCase):
    def test_saveToFile(self):
        # setup
        myClass = ab.argbase()
        myClass.dict['unitTest'] = {'max':10,'min':0,'v':4}

        if(os.path.isfile(myClass.filename)):
            os.remove(myClass.filename)
        # test

        myClass.save()

        # Verify
        os.path.isfile(myClass.filename)

    def test_loadFile(self):
        # setup
        myClass = ab.argbase()

        self.assertEqual(os.path.isfile(myClass.filename), True)
        self.assertEqual( myClass.dict.__len__(), 1)
        #test
        myClass.load()

        #verify
        self.assertEqual(myClass.dict.__len__(), 2)
