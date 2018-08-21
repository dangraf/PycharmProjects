from fastai.structured import *
from fastai.column_data import *
from fastai.lm_rnn import *
from fastai.dataloader import *


def split_by_idx_multi(indexes: np.ndarray, *a):
    """
    Split each array passed as *a, to a pair of arrays like this (elements selected by idxs,  the remaining elements)
    This can be used to split multiple arrays containing training data to validation and training set.

    :param indexes: list of indexes selected
    :param a: list of np.array, each array should have same amount of elements in the first dimension
    :return: list of tuples, each containing a split of corresponding array from *a.
            First element of each tuple is an array composed from elements selected by idxs,
            second element is an array of remaining elements.
    """
    mask = np.zeros(a[0].shape[1], dtype=bool)
    mask[np.array(indexes, dtype=int)] = True
    return [(o[:, mask], o[:, ~mask]) for o in a]


def get_timeseries_index(data_matrix, bptt: int, batch_size: int) -> np.ndarray:
    """
    This function need to be used before using the df in a time series. It re-orders the data
    note, this function expects the index index in the dataframe to be ordered from 0 to datalen

    :param data_matrix: dataframe or matrix to be used for reindexing
    :param bptt: back propagation tru time ( number of samples back in time)
    :param batch_size:  batch size
    :return: list of new index order

    example:
        index = [0,1,2,3,...32]
        bathc size : 4
        bptt = 2

        First chunk of data that should be received in our forward model should be

        iteration 1 in forward function:
        xs[0] = [0,8,16,24]
        xs[1] = [1,9,17,25]
        indexes used:
        index1= [0,1,8,9,16,17,25,25]

        iteration 2 in forward function:
        xs[0] = [3,10,18,26]
        xs[1] = [4,11,19,27]
        indexes used:
        index2 = [3,4,10,11,18,19,26,27]

        iteration 3 in forward function:
        xs[0] = [5,12,20,28]
        xs[1] = [6,13,21,29]
        indexes used:
        index3= [5,6,12,13,20,21,28,29]

        the new index should [index1, index2, index3]
        new_index = [0,1,8,9,16,17,25,25,3,4,10,11,18,19,26,27,5,6,12,13,20,21,28,29....31]
        in that way, it's possible to reshape the dataframe to make the rows of data correctly
        entered the forward function.
        this means that the index need to be orderd as [0,1,8,9,16,17,
    """
    if len(data_matrix) % (bptt * batch_size) != 0:
        raise ValueError(f"datalen:{len(data_matrix)} need to be evenly divided by bptt:{bptt} and batch_size:{batch_size}")
    collen = int(len(data_matrix) / batch_size)
    new_index_order = [batch_start_nbr + k for row_nbr in range(0, collen, bptt) for batch_start_nbr in
                       range(row_nbr, len(data_matrix),collen) for k in range(bptt)]

    return np.asarray(new_index_order,dtype=np.int64)


class PassthruCatAndCont(Dataset):
    def __init__(self, cats, conts, ys, is_reg=True, is_multi=False):
        self.cats = cats
        self.conts = conts
        self.y = ys
        self.is_reg = is_reg
        self.is_multi = is_multi

    def __len__(self):
        return self.y.shape[1]

    def __getitem__(self, idx):
        return [[o[idx] for o in self.cats], [o[idx] for o in self.conts], self.y[:, idx]]


class PassthruTimeseries(Dataset):
    def __init__(self, xs, ys, is_reg=True, is_multi=False):
        self.xs, self.y = xs, ys
        self.is_reg = is_reg
        self.is_multi = is_multi

    def __len__(self):
        return self.y.shape[1]

    def __getitem__(self, idx):
        return [[o[idx] for o in self.xs], self.y[:, idx]]


class ColumnarTimeseriesData(ModelData):
    def __init__(self, path, trn_ds, val_ds, bs, test_ds=None, shuffle=False):
        test_dl = DataLoader(test_ds, bs, shuffle=shuffle, num_workers=1,
                             transpose_y=True) if test_ds is not None else None

        super().__init__(path, DataLoader(trn_ds, bs, shuffle=shuffle, num_workers=1, transpose_y=True),
                         DataLoader(val_ds, bs * 2, shuffle=False, num_workers=1, transpose_y=True), test_dl)

    @classmethod
    def from_arrays(cls, path, val_idxs, xs, y, is_reg=True, is_multi=False, bs=64, test_xs=None, shuffle=False):
        ((val_xs, trn_xs), (val_y, trn_y)) = split_by_idx_multi(val_idxs, xs, y)
        test_ds = PassthruTimeseries(*test_xs, [0] * len(test_xs), is_reg=is_reg,
                                     is_multi=is_multi) if test_xs is not None else None
        return cls(path, PassthruTimeseries(trn_xs, trn_y, is_reg=is_reg, is_multi=is_multi),
                   PassthruTimeseries(val_xs, val_y, is_reg=is_reg, is_multi=is_multi),
                   bs=bs, shuffle=shuffle, test_ds=test_ds)

    @classmethod
    def from_dataframe(cls, path, val_ratio, df, cat, cont, y_name, bptt, bs, do_scale=True):
        """
        :param path:
        :param val_ratio: how large part of the dataset to be used for validation,  usually set to 0.2 to 0.3
        :param df:  dataframe containing all data
        :param cat: list of catergorical columns
        :param cont: list of continous columns
        :param y_name:  name of column to predict
        :param bppt: back propagate thru time
        :param bs:
        :param is_multi:
        :return:
        """

        cols = cat + cont if cat is not None and cont is not None else cont if cat is None else cat
        # todo fill in values in dataframe if bs and bppt does not divide evenly. set them as NaN



        # change categories to correct type
        for v in cat: df[v] = df[v].astype('category').cat.as_ordered()

        # replace NaN with zeros
        for v in cont:
            df[v] = df[v].fillna(0).astype('float32')
        # replace categories with numbers and scale continous variables
        df = df.sort_index()  # make sure that the rows have not been re-ordered.
        new_index = get_timeseries_index(df=df, bptt=bptt, batch_size=bs)
        df = df.reindex(new_index)

        df2, y, nas, mapper = proc_df(df, y_name, do_scale=True)


        num_cols = len(cols)  #
        xs_cat = df2[cat].values.reshape(-1, bptt, len(cat))
        xs_cont = df2[cont].values.reshape(-1, bptt, len(cont))

        xs_cat = xs_cat.swapaxes(1, 0)
        xs_cont = xs_cont.swapaxes(1, 0)

        ys = y.reshape(-1, bptt).T

        # make sure the validation split is between two batches
        num_batches = int(len(df)/(bptt*bs))
        val_start = round(num_batches*bs*(1-val_ratio))
        val_idx = list(range(val_start, num_batches*bs))
        (val_xs_cat, trn_xs_cat), (val_xs_cont, trn_xs_cont), (val_y, trn_y) = split_by_idx_multi(val_idx, xs_cat,
                                                                                                  xs_cont, ys)

        # todo tests, cat = None elller cont = None
        return cls(path, PassthruCatAndCont(trn_xs_cat, trn_xs_cont, ys=trn_y, is_reg=True, is_multi=True),
                   PassthruCatAndCont(val_xs_cat, val_xs_cont, ys=val_y, is_reg=True, is_multi=True),
                   bs=bs, shuffle=False, test_ds=None)
