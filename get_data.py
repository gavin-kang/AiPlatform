from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

import numpy as np
import pandas as pd
import tensorflow as tf
import os


def raw_dataframe(URL, column_types, na_val):
    """get file data as dataframe
    args：
      URL:file url，web path support
      column_types: all the columns in the file
      na_val: the string for none values in the file
    """
    file_name = os.path.split(URL)[-1]
    file_ext = file_name.split('.')[-1]
    path = tf.keras.utils.get_file(file_name, URL)
    ordered_column = collections.OrderedDict(column_types)
    if file_ext == '.csv':
        df = pd.read_csv(path, names=ordered_column.keys(),
                         dtype=ordered_column, na_values=na_val)
    elif file_ext == '.xls' or file_ext == '.xlsx':
        df = pd.read_excel(path, names=ordered_column.keys(),
                           dtype=ordered_column, na_values=na_val)
    else:
        raise Exception("仅支持excel和csv格式的数据类型", file_ext)
    return df


def load_data(URL, column_types, na_val,y_name="y", train_fraction=0.7, seed=None):
    """
    load data from file
    """
    # Load the raw data columns.
    file_name = os.path.split(URL)[-1]
    file_ext = file_name.split('.')[-1]
    path = tf.keras.utils.get_file(file_name, URL)
    ordered_column = collections.OrderedDict(column_types)
    if file_ext == '.csv':
        data = pd.read_csv(path, names=ordered_column.keys(),
                         dtype=ordered_column, na_values=na_val)
    elif file_ext == '.xls' or file_ext == '.xlsx':
        data = pd.read_excel(path, names=ordered_column.keys(),
                           dtype=ordered_column, na_values=na_val)
    else:
        raise Exception("仅支持excel和csv格式的数据类型", file_ext)

    # Delete rows with unknowns
    data = data.dropna()
    # Shuffle the data
    np.random.seed(seed)
    # Split the data into train/test subsets.
    x_train = data.sample(frac=train_fraction, random_state=seed)
    x_test = data.drop(x_train.index)

    # Extract the label from the features DataFrame.
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
