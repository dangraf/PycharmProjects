import unittest
import PrepareData
import numpy as np
import pandas as pd
from hypothesis import given
import hypothesis.extra.numpy as hypnumpy
from hypothesis.strategies import floats
import pyvalid
from sklearn import preprocessing
from pandas.util.testing import assert_almost_equal


class TestSequenceFunctions(unittest.TestCase):
    @given(hypnumpy.array_shapes(min_dims=1, max_dims=3, min_side=5, max_side=10))
    def test_Split_check_Dimentions(self, arrayShape):
        print(arrayShape)
        # setup
        # Create random shape array containint random numbers
        array = np.ndarray(arrayShape)
        seq_len = 2
        expectedNumDim = len(arrayShape)+1

        # test
        output = PrepareData.split_sequential_df_to_matrix(array, seq_len)

        # verify
        outshape = output.shape
        numdim=  len(outshape)
        self.assertEqual(numdim, expectedNumDim)
        expected_length = arrayShape[0]+1-seq_len
        self.assertEqual(outshape[0], expected_length)
        self.assertEqual(outshape[1], seq_len)

        iterdims = iter(arrayShape)
        next(iterdims)
        for i, input_dim in enumerate(iterdims):
            self.assertEqual(input_dim, outshape[i+2])

    @given(hypnumpy.arrays(np.float, (12, 5), elements=floats(17, 100)))
    def test_normalize_inverse_dataframe(self, array):
        # setup
        df = pd.DataFrame(array)
        scalar = preprocessing.StandardScaler()
        df_temp = PrepareData.normalize_dataframe(df, scalar, inverce=False)

        # test
        df_out = PrepareData.normalize_dataframe(df_temp, scalar, inverce=True)

        # verify
        assert_almost_equal(df, df_out)

    @given(hypnumpy.arrays(np.float, (10, 2), elements=floats(17, 100)))
    def test_normalize_dataframe(self, array):
        # setup
        array[0, :] = 7
        df = pd.DataFrame(array)
        expected_columns = ['one', 'two']
        df.columns = expected_columns
        scalar = preprocessing.StandardScaler()
        # test
        df_out = PrepareData.normalize_dataframe(df, scalar, inverce=False)

        # verify for each columns
        col1_mean = df_out.mean()
        col1_std = df_out.std()
        # verify that std and mean==0 and std almost 1.0
        self.assertAlmostEqual(col1_mean[0], 0.0, places=3)
        self.assertAlmostEqual(col1_std[0], 1.0, places=0)
        # check that column names are same as input dataframe
        self.assertEqual(list(df.columns), expected_columns)
        # new dataframe shold be a copy
        self.assertFalse( df.equals(df_out) )


    def test_split_wrong_input_type(self):
        # setup
        # test and verify
        with self.assertRaises(pyvalid.ArgumentValidationError):
            PrepareData.split_sequential_df_to_matrix("hej", 3)


    #hypothesis.extra.numpy.array_shapes(min_dims=1, max_dims=3, min_side=1, max_side=10)
    def test_split_sequential_df_to_matrix(self):
        # setup
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=np.int)
        df = pd.DataFrame(data)

        # test
        output = PrepareData.split_sequential_df_to_matrix(df, 3)

        # verify
        expected = np.array([[[1], [2], [3]],
                             [[2], [3], [4]],
                             [[3], [4], [5]],
                             [[4], [5], [6]],
                             [[5], [6], [7]],
                             [[6], [7], [8]]], dtype=np.int)
        notexpected = np.array([[[1], [2], [3]],
                             [[2], [3], [4]],
                             [[3], [4], [5]],
                             [[4], [5], [6]],
                             [[5], [6], [7]],
                             [[6], [7], [9]]], dtype=np.int)    # note, 8 is changed to 9
        # verify result
        self.assertTrue((output == expected).all())
        # verify verification method
        self.assertFalse((output == notexpected).all())
