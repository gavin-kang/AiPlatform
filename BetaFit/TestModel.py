# -*- coding:utf-8 -*-
# @Time    : 2018/6/9 14:11
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : TestModel.py
# @Software: PyCharm

from BetaFit.model import BetaModel
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir('C:\\Users\\T480S\\work\\AiPlatform\\BetaFit')
total_data = pd.read_csv("data.csv")

data_one = total_data['1号机组调速器压力油罐油位']
data = total_data['1号机组调速器压力油罐油位'][40000:]
a, b, d1, d2 = BetaModel(data)

# 滤波
tdata = data[0:1000]
cycle, trend = sm.tsa.filters.hpfilter(tdata, 1600)

# 画图
# 1 拟合图
# 2 原始直方图
plt.figure(2)
plt.hist(data, bins=30, normed=True)
plt.vlines(d1, 0, 0.006, colors="r", linestyles="dashed")
plt.vlines(d2, 0, 0.006, colors="r", linestyles="dashed")
plt.show()

# 3 原始数据+阈值区间
plt.figure(3)
xline = range(len(data_one))
plt.plot(xline, data_one)
plt.hlines(d1, 0, max(xline), colors="r", linestyles="dashed")
plt.hlines(d2, 0, max(xline), colors="r", linestyles="dashed")
plt.show()

# 4 原始与滤波后对比
plt.figure(4)
plt.plot(range(len(tdata)), trend, color='r')
plt.plot(range(len(tdata)), tdata)
plt.show()