# -*- coding:utf-8 -*-
# @Time    : 2018/6/20 16:11
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : qushu1.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'k']
total_data = pd.read_csv('./data/20180620.csv', header=None)


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


def guiyi(x):
    Min, Max = min(x), max(x)
    x = (x - Min) / (Max - Min)
    return x


hour_data = qushu(total_data, 360)
# file_path = 'data/hour_data.csv'
# hour_data.to_csv(file_path, encoding='utf-8', index=False)

qdata = total_data[460000:]
name = ['1号机组调速器压力油罐油压', '1号机组调速器压力油罐油位', '1号机组调速器回油箱油位',
        '1号机组有功(有功变送器1)', '1号机组有功(有功变送器2)', '1号机组导叶开度(SJ30)']
extra = '一年'
plt.figure(figsize=(15, 8))
for i in range(1, 7):
    j = 32*10 + i
    plt.subplot(j)
    plt.plot(qdata[i])
    plt.title(name[i-1]+extra)
plt.show()
