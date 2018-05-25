from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

import numpy as np
import pandas as pd
import tensorflow as tf
import os


def raw_dataframe(file_path):
    """get file data as dataframe
    args：
      URL:file url，web path support
      column_types: all the columns in the file
      na_val: the string for none values in the file
    """
    file_ext = os.path.splitext(file_path)[-1]
    if file_ext == '.csv':
        df = pd.read_csv(file_path)
    elif file_ext == '.xls' or file_ext == '.xlsx':
        df = pd.read_excel(file_path)
    else:
        raise Exception("仅支持excel和csv格式的数据类型", file_ext)
    return df


def load_data(file_data=None,file_path=None,y_name="Y", train_fraction=0.7, seed=None):
    """
    加载数据集
    """
    if file_data:
        data=file_data
    else:
        data=raw_dataframe(file_path)
    data = data.dropna()
    np.random.seed(seed)
    x_train = data.sample(frac=train_fraction, random_state=seed)
    x_test = data.drop(x_train.index)
    y_train = x_train.pop(y_name)
    y_test = x_test.pop(y_name)
    return (x_train, y_train), (x_test, y_test)


def make_dataset(x, y=None):
    """Create a slice Dataset from a pandas DataFrame and labels"""
    # TODO(markdaooust): simplify this after the 1.4 cut.
    # Convert the DataFrame to a dict
    x = dict(x)

    # Convert the pd.Series to np.arrays
    for key in x:
        x[key] = np.array(x[key])

    items = [x]
    if y is not None:
        items.append(np.array(y, dtype=np.float32))

    # Create a Dataset of slices








    return tf.data.Dataset.from_tensor_slices(tuple(items))
