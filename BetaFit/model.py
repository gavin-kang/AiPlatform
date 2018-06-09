# -*- coding:utf-8 -*-
# @Time    : 2018/6/8 22:27
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : model.py
# @Software: PyCharm

from scipy.stats import beta
from scipy.special import gamma as gammaf
import statsmodels.api as sm
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


# 滤波函数
def HpFilter(dta):
    cycle, trend = sm.tsa.filters.hpfilter(dta, 15000)
    return cycle, trend


# model运行主函数
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



