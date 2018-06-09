# -*- coding:utf-8 -*-
# @Time    : 2018/6/8 22:27
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : model.py
# @Software: PyCharm

from scipy.stats import beta
from scipy.special import gamma as gammaf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

os.chdir('C:\\Users\\T480S\\work\\AiPlatform\\BetaFit')
total_data = pd.read_csv("data.csv")


def MaxMinNormalization(x):
    Min, Max = min(x), max(x)
    x = (x - Min) / (Max - Min)
    return x


def betaNLL(param, *args):

    a, b = param
    data = args[0]
    pdf = beta.pdf(data, a, b, loc=0, scale=1)
    lg = np.log(pdf)
    # -----Replace -inf with 0s------
    lg = np.where(lg == -np.inf, 0, lg)
    nll = -1*np.sum(lg)
    return nll


def BetaModel(data):

    def fitted(x, a, b):
        fx = gammaf(a+b)/gammaf(a)/gammaf(b)*x**(a-1)*(1-x)**(b-1)  # pdf of beta
        return fx

    data1 = MaxMinNormalization(data)

    a, b, xx, yy = beta.fit(data1)

    plt.hist(data1, bins=30, normed=True)
    xx = np.linspace(0, max(data1), len(data1))
    plt.plot(xx, fitted(xx, a, b), 'g')
    plt.show()

    alpha = 0.99
    q1, q2 = beta.interval(alpha, a, b, loc=0, scale=1)

    d1 = q1*(max(data)-min(data))+min(data)
    d2 = q2*(max(data)-min(data))+min(data)

    return a, b, d1, d2


# 测试
data = total_data['1号机组调速器压力油罐油位'][40000:]
a, b, d1, d2 = BetaModel(data)

# 画图
# 1 拟合图
# 2 原始直方图
plt.figure(2)
plt.hist(data, bins=30, normed=True)
plt.vlines(d1, 0, 0.006, colors="r", linestyles="dashed")
plt.vlines(d2, 0, 0.006, colors="r", linestyles="dashed")
plt.show()

plt.figure(3)
xline = range(len(total_data['1号机组调速器压力油罐油位']))
plt.plot(xline, total_data['1号机组调速器压力油罐油位'])
plt.hlines(d1, 0, max(xline), colors="r", linestyles="dashed")
plt.hlines(d2, 0, max(xline), colors="r", linestyles="dashed")
plt.show()
