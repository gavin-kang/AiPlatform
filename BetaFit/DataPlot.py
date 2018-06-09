# -*- coding:utf-8 -*-
# @Time    : 2018/6/8 11:26
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : DataPlot.py
# @Software: PyCharm

from scipy.optimize import fmin
from scipy.stats import beta
from scipy.special import gamma as gammaf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os

os.chdir('C:\\Users\\T480S\\work\\AiPlatform\\BetaFit')
total_data = pd.read_csv("data.csv")

# 解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(1)
xt = range(len(total_data))
plt.subplot(321)
plt.plot(xt, total_data['1号机组上止漏环出口压力'])
plt.title('1号机组上止漏环出口压力')

plt.subplot(322)
plt.plot(xt, total_data['1号机组水头'])
plt.title('1号机组水头')

plt.subplot(323)
plt.plot(xt, total_data['1号机组调速器压力油罐油压'])
plt.title('1号机组调速器压力油罐油压')

plt.subplot(324)
plt.plot(xt, total_data['1号机组调速器压力油罐油位'])
plt.title('1号机组调速器压力油罐油位')

plt.subplot(313)
plt.plot(xt, total_data['1号机组调速器回油箱油位'])
plt.title('1号机组调速器回油箱油位')
plt.show()


plt.figure(2)
plt.subplot(321)
sns.distplot(total_data['1号机组上止漏环出口压力'][40000:])
plt.subplot(322)
sns.distplot(total_data['1号机组水头'][40000:])
plt.subplot(323)
sns.distplot(total_data['1号机组调速器压力油罐油压'][40000:])
plt.subplot(324)
sns.distplot(total_data['1号机组调速器压力油罐油位'][40000:])
plt.subplot(313)
sns.distplot(total_data['1号机组调速器回油箱油位'][40000:])
plt.show()






