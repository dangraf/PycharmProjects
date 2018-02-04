from unittest import TestCase

from Projects.mongo_data.mongo_init import init_mongodb
from Projects.mongo_data.settings_data import get_safe_settingslist, get_settingslist
from Projects.mongo_data.ticker_data import save_tickerdata, get_TickerSettings


init_mongodb()

class TestMongoOperations(TestCase):
    def test_settings_data(self):
        # prepare by removing the testlist
        mylist = get_settingslist('testList')
        if mylist is not None:
            mylist.delete()
            mylist = get_settingslist('testList')
            self.assertTrue(mylist is None)

        # create a default list
        defaultparams = ['apa','bepa','cepa']
        mylist = get_safe_settingslist('testList', defaultparams)
        # verify that we receive a default list object
        self.assertEqual(mylist.name, 'testList')
        self.assertCountEqual( mylist.list, defaultparams)
        self.assertEqual(mylist.list[0], 'apa')
        # check that the list was properly saved into database
        mylist = get_settingslist('testList')
        self.assertEqual(mylist.name, 'testList')
        self.assertCountEqual(mylist.list, defaultparams)
        self.assertEqual(mylist.list[0], 'apa')
        # cleanup
        mylist.delete()
        mylist = get_settingslist('testList')
        self.assertTrue(mylist is None)
        pass

    def test_save_ticker_data(self):
        mydata = {'namn': 5, 'id': 5.7, 'apa': 'Tjohej'}
        save_tickerdata(mydata, 'testcol')
        pass

    def test_get_ticker_settings(self):

        allsettings = get_TickerSettings()
        self.assertEqual(len(allsettings),4)