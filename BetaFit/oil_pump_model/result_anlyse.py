# -*- coding:utf-8 -*-
# @Time    : 2018/6/22 11:52
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : result_anlyse.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans

gap1 = pd.read_csv('./data/gap0.csv', header=None)
gap2 = pd.read_csv('./data/gap1.csv', header=None)

# data = gap1.values.reshape(-1, 1)
# clf = KMeans(n_clusters=2, max_iter=300, n_init=10)
# clf.fit(data)
# ypred = clf.fit_predict(data)
# result = pd.DataFrame([gap1.values, ypred]).T
#
# plt.scatter(range(len(gap1)), gap1, c=ypred)
# plt.show()

g1 = gap1[gap1 < 100]
g2 = gap2[gap2 < 100]

g1.dropna(inplace=True)
g11 = pd.Series(g1.iloc[:, 0].values)
g2.dropna(inplace=True)
g22 = pd.Series(g2.iloc[:, 0].values)


# plt.figure(2)
# plt.hist(g11, bins=100, normed=True)
# plt.xlim((0, 50))
# plt.show()

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def data_count(dataa, r1, r2, step):
    r = pd.DataFrame(np.random.randn(1, 2))
    r.drop(0, inplace=True)
    while r1+step <= r2:
        num = 0
        for j in range(len(dataa)):
            if dataa[j] >= r1 and dataa[j] < r1+step:
                num = num + 1
        f = "%s~%d" % (r1, r1+step)
        # r = r.append([[int(r1), num], ]) # 使用单数表示
        r = r.append([[f, num], ])  # 使用范围表示
        r1 = r1 + step
    return r


def plot_bar(plot_data, title):
    plt.figure(figsize=(10, 15))
    y = plot_data.iloc[:, 1].values
    tt = list(range(len(y)))
    index = plot_data.iloc[:, 0].values
    plt.bar(left=0, bottom=list(range(len(y))), width=y, color='blue', height=0.5,
            orientation='horizontal')  # 水平对应bottom&width， height表示bar的宽度
    plt.yticks(tt, index)
    plt.ylabel('数据值')
    plt.xlabel('频数')
    plt.title(title)
    plt.show()


data_gap1 = data_count(g11[:], 1, 51, 1)
data_gap2 = data_count(g22[:], 1, 51, 1)
plot_bar(data_gap1, title='工况1')
plot_bar(data_gap2, title='工况2')

# 保存数据
data_gap1.to_csv('./data/工况1数据.csv', encoding='utf-8', index=False)
data_gap2.to_csv('./data/工况2数据.csv', encoding='utf-8', index=False)
