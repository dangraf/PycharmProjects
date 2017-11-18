from unittest import TestCase
from bitcoin_news import ParseBitcoinNews
from datetime import datetime
from datetime import timedelta


class TestParseBitcoinNews(TestCase):
    def test__isNewData_in_empty_list(self):
        # prepare
        a = ParseBitcoinNews()
        newdata = {'text': 'new_text', 'time': datetime.now()}
        # test
        result = a._is_new_data(newdata)
        # verify
        self.assertEqual(result, True)

    def test__isNewData_when_already_in_list(self):
        # prepare
        a = ParseBitcoinNews()
        newdata1 = {'text': 'new_text', 'time': datetime.now()}
        newdata2 = {'text': 'new_text', 'time': datetime.now() + timedelta(seconds=5)}
        a.histData.append(newdata1)
        # test
        result = a._is_new_data(newdata2)
        # verify
        self.assertEqual(result, False)

    def test__deleteOldData_no_data(self):
        # prepare
        a = ParseBitcoinNews()
        # test
        a._delete_old_data()
        # verify

    def test__deleteOldData_when_old(self):
        # prepare
        a = ParseBitcoinNews()
        newdata = {'text': 'new_text', 'time': datetime.now() - timedelta(hours=27)}
        a.histData.append(newdata)
        # test
        a._delete_old_data()
        # verify
        self.assertEqual(len(a.histData), 0)

    def test__deleteOldData_when_new(self):
        # prepare
        a = ParseBitcoinNews()
        newdata = {'text': 'new_text', 'time': datetime.now()}
        a.histData.append(newdata)
        # test
        a._delete_old_data()
        # verify
        self.assertEqual(len(a.histData), 1)

    def test_check_for_news(self):
        # prepare
        a = ParseBitcoinNews()
        # test
        a.check_for_news()
        self.assertEqual(len(a.histData), 5)

    def test__is_new_data2(self):
        newdata = {'text': 'new_text', 'time': datetime.now()}
        a = ParseBitcoinNews()
        ret = a._is_new_data2(newdata)
        self.assertEqual(ret, True)


