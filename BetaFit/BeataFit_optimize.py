# -*- coding:utf-8 -*-
# @Time    : 2018/6/8 14:02
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : BeataFit_optimize.py
# @Software: PyCharm

from scipy.optimize import fmin
from scipy.stats import beta
from scipy.special import gamma as gammaf
import matplotlib.pyplot as plt
import numpy as np

# 归一化
def MaxMinNormalization(x):
    Min, Max = min(x), max(x)
    x = (x - Min) / (Max - Min)
    return x

# 随机生成数据(220+-22)
mu, sigma, sampleNo = 220, 20, 1000
s = np.random.normal(mu, sigma, sampleNo)
# plt.hist(s, 30, normed=True)
# plt.show()

data = MaxMinNormalization(s)

# 计算参数
# 1 计算均值和参数
xmean = np.mean(data)
xvar = np.var(data)

# data排序
