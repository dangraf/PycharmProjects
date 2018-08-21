from unittest import TestCase
from fastai.structured import *
from fastai.column_data import *
from fastai.lm_rnn import *
from fastai.dataloader import *
from dl_fastai.columnar_timeseries import *


# from fastai.columnar_timeseries import *

def get_df(datalen):
    df = pd.DataFrame()
    df['A'] = np.arange(datalen)
    df['B'] = np.arange(datalen) * 10
    df['C'] = np.arange(datalen) * 100
    df['D'] = np.random.choice(a=[True, False], size=datalen)
    df['out'] = np.arange(datalen)
    return df


class TestColumnarTimeseriesData(TestCase):
    def setUp(self):
        cs = 2
        datalen = 64
        columns = 4
        a = np.arange(0, datalen).reshape(-1, cs, columns)
        self.xs = a.swapaxes(1, 0)
        self.ys = np.arange(0, int(datalen / columns)).reshape(-1, cs).T
        self.val_idx = np.arange(len(a) - 2, len(a))

    def test_verify_vector_sizes(self):
        self.assertEqual(self.xs.shape[0], 2)  # two timesteps in time
        self.assertEqual(self.xs.shape[1], 8)  # 8 rows of data
        self.assertEqual(self.xs.shape[2], 4)  # cor columns
        self.assertEqual(self.ys.shape[0], 2)  # data for both time steps
        self.assertEqual(self.ys.shape[1], 8)  # 8 rows of data

    def test_split_data(self):
        ((val_xs, trn_xs), (val_y, trn_y)) = split_by_idx_multi(self.val_idx, self.xs, self.ys)
        self.assertEqual(val_xs.shape[1], 2)
        self.assertEqual(trn_xs.shape[1], 6)  # number of elements in list
        self.assertEqual(trn_xs.shape[2], 4)  # number of columns has not changed

        self.assertEqual(val_y.shape[1], 2)
        self.assertEqual(trn_y.shape[1], 6)

    def test_PassthruTimeseries_single_index(self):
        data_sync = PassthruTimeseries(self.xs, self.ys)
        (x, y) = data_sync[0]
        # now, x and y are lists
        self.assertEqual(len(x), 2)
        self.assertEqual(len(x[0]), 4)
        # this might be a bit strange, if we just have one number as index, we might expect an array of size 2,1,4
        # and when we have an array of 3 indexes we would like to expect 2,3,4
        self.assertEqual(len(y), 2)

    def test_PassthruTimeseries_multi_index(self):
        data_sync = PassthruTimeseries(self.xs, self.ys)
        idxs = np.arange(2, 5)  # [2,3,4]
        (x, y) = data_sync[idxs]
        # now, x and y are lists
        self.assertEqual(len(x), 2)
        self.assertEqual(len(x[0]), 3)

        self.assertEqual(len(y), 2)
        self.assertEqual(len(y[0]), 3)
        # this might be a bit strange, if we just have one number as index, we might expect an array of size 2,1,4
        # and when we have an array of 3 indexes we would like to expect 2,3,4

    def test_PassthruCatAndCont_multi_index(self):
        data_sync = PassthruCatAndCont(cats=self.xs[:, :, 0:3], conts=self.xs[:, :, 3], ys=self.ys)
        idxs = np.arange(2, 6)
        (cat, cont, y) = data_sync[idxs]
        self.assertEqual(len(cat), 2)
        self.assertEqual((len(cat[0])), 4)

    def test_dataloader_returns_y_correct(self):
        data_sync = PassthruTimeseries(self.xs, self.ys)
        dl = DataLoader(data_sync, batch_size=4, shuffle=True, num_workers=1, transpose_y=True)
        x, y = next(iter(dl))
        self.assertEqual(len(y[0]), 4)

    def test_ColumnarTimeseriesData(self):
        dl = ColumnarTimeseriesData.from_arrays(path='.', val_idxs=self.val_idx, xs=self.xs, y=self.ys, bs=4)
        (x, y) = next(iter(dl.trn_dl))
        self.assertEqual(len(x), 2)
        self.assertEqual(len(y), 2)
        self.assertEqual(len(y[0]), 4)

        # verify
        self.assertEqual(len(x), 2)

    def test_get_timeseries_index(self):
        # Setup dataframe as test-object
        df = get_df(datalen=16)

        # test for bptt=2
        index = get_timeseries_index(df=df, bptt=2, batch_size=4)
        self.assertEqual(index[0], 0)
        self.assertEqual(index[1], 1)
        self.assertEqual(index[2], 4)
        self.assertEqual(index[3], 5)
        self.assertEqual(index[4], 8)
        self.assertEqual(index[5], 9)
        self.assertEqual(index[6], 12)
        self.assertEqual(index[7], 13)

        # test for bptt=4
        index = get_timeseries_index(df=df, bptt=4, batch_size=2)
        self.assertEqual(index[0], 0)
        self.assertEqual(index[1], 1)
        self.assertEqual(index[2], 2)
        self.assertEqual(index[3], 3)
        self.assertEqual(index[4], 8)
        self.assertEqual(index[5], 9)
        self.assertEqual(index[6], 10)
        self.assertEqual(index[7], 11)

        # test wrong length
        with self.assertRaises(ValueError):
            get_timeseries_index(df, bptt=3, batch_size=4)
            self.fail('Should have rised an Value error since 16 is not evenly divided by 3')

    def test_columnar_timeseries_from_df(self):
        # setup data
        df = get_df(32)
        columns = ['A', 'B', 'C']
        num_cols = len(columns)
        bptt = 2
        df_train = df[columns].copy()
        ys = df['out'].values
        bs = 4
        new_index = get_timeseries_index(df=df_train, bptt=bptt, batch_size=bs)
        df_train = df_train.reindex(new_index)
        df_train.reset_index(drop=True, inplace=True)

        xs = df_train.values.reshape(-1, bptt, num_cols)
        xs = xs.swapaxes(1, 0)
        ys = ys.reshape(-1, bptt).T

        val_idx = np.arange(int(len(df) / bptt) - bs, int(len(df) / bptt))

        # test
        dl = ColumnarTimeseriesData.from_arrays(path='.',
                                                val_idxs=val_idx,
                                                xs=xs,
                                                y=ys,
                                                bs=bs)
        for x, y in dl.trn_dl:
            print(x)
            print(y)
        x1, y1 = next(iter(dl.trn_dl))
        print(x1)

    def test_columnar_with_real_dataframe(self):
        df = get_df(32)
        dl = ColumnarTimeseriesData.from_dataframe(path='.', val_ratio=0.25, df=df, cat=['D'], cont=['A', 'B'],
                                                   y_name='C', bptt=2, bs=4, do_scale=False)

        x_cat, x_cont, y = next(iter(dl.trn_dl))
        # check sizes of data
        self.assertEqual(len(x_cat), 2)     # bptt
        self.assertEqual(len(x_cont), 2)    # bptt
        self.assertEqual(len(y), 2)

        self.assertEqual(len(x_cat[0]), 4)  # batch size
        self.assertEqual(len(x_cont[0]), 4)  # batch size
        self.assertEqual(len(y[0]), 4)

        self.assertEqual(len(x_cat[0][0]), 1)  # num columns ('D')
        self.assertEqual(len(x_cont[0][0]), 2)  # num columns ('A, 'B')

        # check order of data
        self.assertEqual(y[0,0], 0)
        self.assertEqual(y[0, 1], 800)
        self.assertEqual(y[0, 2], 1600)
        self.assertEqual(y[0, 3], 2400)

        self.assertEqual(y[1, 0], 100)
        self.assertEqual(y[1, 1], 900)

    get_cv_idxs()




