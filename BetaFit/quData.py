# -*- coding:utf-8 -*-
# @Time    : 2018/6/12 10:11
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : quData.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'k']
total_data = pd.read_csv('../BetaFit/wb_20180612.csv', header=None)


def qushu(qdata, gap):
    i, j = 0, 0
    long = len(qdata.columns)
    gap_data = pd.DataFrame(np.random.randn(1, long))
    gap_data.drop(0, inplace=True)

    while i <= len(qdata):
        gap_data = gap_data.append(qdata.iloc[i, :])
        i = i + gap
    gap_data.index = range(len(gap_data))
    return gap_data


minute_data = qushu(total_data, 60)
file_path = 'BetaFit/minute_data.csv'
# minute_data.to_csv(file_path, encoding='utf-8', index=False)

data1 = minute_data.iloc[:, 1]
data2 = minute_data.iloc[:, 2]
data3 = minute_data.iloc[:, 3]
data4 = minute_data.iloc[:, 4]
data5 = minute_data.iloc[:, 5]

plt.figure(figsize=(20, 5))
plt.subplot(231)
plt.plot(data1)
plt.subplot(232)
plt.plot(data2)
plt.subplot(233)
plt.plot(data3)
plt.subplot(234)
plt.plot(data4)
plt.subplot(235)
plt.plot(data5)
plt.show()
