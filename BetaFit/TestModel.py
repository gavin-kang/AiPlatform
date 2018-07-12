# -*- coding:utf-8 -*-
# @Time    : 2018/6/9 14:11
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : TestModel.py
# @Software: PyCharm

from BetaFit.model import BetaModel
import statsmodels.api as sm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

total_data = pd.read_csv("../BetaFit/data.csv")
# 解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data_one = total_data['1号机组调速器压力油罐油位']
data = total_data['1号机组调速器压力油罐油位'][40000:]
a, b, d1, d2 = BetaModel(data)


# 滤波
tdata = data[0:1000]
cycle, trend = sm.tsa.filters.hpfilter(tdata, 1600)
cycle1, trend1 = sm.tsa.filters.hpfilter(data_one, 1600)


# 阈值测试
def abnormal(shuju, qujian1, qujian2):
    zc, yc = [], []
    for i in range(len(shuju)):
        if (shuju.values[i] > qujian1 and shuju.values[i] < qujian2):
            zc.append(shuju.values[i])
        else:
            yc.append(shuju.values[i])
    return zc, yc


# 生成异常数据
ab_data = total_data['1号机组调速器压力油罐油位'][40000:]
ab_data.index = range(len(ab_data))
eed = len(ab_data)
jb = list(np.arange(0., 200., 0.1))
one1 = list(np.ones(len(ab_data[17535:eed])))
ab_data[15535:17535] = ab_data[15535:17535].add(jb, axis=0)
ab_data[17535:eed] = ab_data[17535:eed].add(one1, axis=0)

# 异常识别
zc, yc = abnormal(data, d1, d2)
zc_hp, yc_hp = abnormal(trend, d1, d2)
rate_nhp = len(yc)/(len(zc)+len(yc))
rate_hp = len(yc_hp)/(len(zc_hp)+len(yc_hp))


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
plt.plot(xline, data_one, label='滤波前')
plt.plot(range(len(trend1)), trend1, color='r', label='滤波后')
plt.hlines(d1, 0, max(xline), colors="r", linestyles="dashed")
plt.hlines(d2, 0, max(xline), colors="r", linestyles="dashed")
plt.legend()
plt.title('原始数据滤波前后与阈值对比')
plt.show()


# 4 原始与滤波后对比
plt.figure(4)
plt.plot(range(len(tdata)), trend, color='r')
plt.plot(range(len(tdata)), tdata)
plt.show()

# 5 滤波前后异常识别
plt.figure(5)
plt.subplot(211)
plt.scatter(range(len(zc)), zc)
plt.scatter(range(len(yc)), yc, color='r')
plt.subplot(212)
plt.scatter(range(len(zc_hp)), zc_hp)
plt.scatter(range(len(yc_hp)), yc_hp, color='r')
plt.show()

# 6 滤波前后异常识别率对比

# 7
