# -*- coding:utf-8 -*-
# @Time    : 2018/6/22 16:39
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : operating_condition_classify.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D


# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def oc_clasf(total_data):
    # 数据预处理
    name = ['时间', '1号机组调速器压力油罐油压', '1号机组调速器压力油罐油位', '1号机组调速器回油箱油位',
            '1号机组有功(有功变送器1)', '1号机组有功(有功变送器2)', '1号机组导叶开度(SJ30)']
    # total_data = pd.read_csv('./data/20180620.csv', header=None)
    x0 = total_data[0][30000:460000]
    x1 = total_data[1][30000:460000]
    x2 = total_data[5][30000:460000]
    x3 = total_data[6][30000:460000]
    # 剔除异常数据
    id1 = list(x1[x1 < 5.5].index)
    id2 = list(x2[x2 < -5].index)
    id3 = list(x3[x3 < -2].index)
    idd = id1+id2+id3
    x1.drop(idd, inplace=True)
    x2.drop(idd, inplace=True)
    x3.drop(idd, inplace=True)
    x0.drop(idd, inplace=True)

    # # 散点图展示
    # # x2和x3
    # plt.scatter(x1[:], x2[:])
    # plt.xlabel('1号机组调速器压力油罐油压')
    # plt.ylabel('1号机组有功(有功变送器2)')
    # plt.show()
    # # x1,x2,x3
    # ax = plt.subplot(111, projection='3d')
    # ax.scatter(x2, x3, x1)
    # ax.set_zlabel('1号机组调速器压力油罐油压')  # 坐标轴
    # ax.set_ylabel('1号机组导叶开度(SJ30)')
    # ax.set_xlabel('1号机组有功(有功变送器2)')
    # plt.show()

    # k-means 聚类
    data = pd.DataFrame([x2, x3]).values.T
    clf = KMeans(n_clusters=2, max_iter=300, n_init=10)
    clf.fit(data)
    # ypred = clf.predict(data)
    ypred = clf.fit_predict(data)
    # cl = ypred.reshape(-1, 1)


    # # 分类结果展示
    # q = 1000
    # showdata = data[:q]
    # cl1 = ypred[:q]
    # plt.scatter(showdata[:, 0], showdata[:, 1], c=cl1)
    # plt.show()

    # 油压分类
    q = 10000
    xshow1 = x1[:q]
    cl2 = ypred[:q]
    plt.scatter(range(len(xshow1)), xshow1, c=cl2)
    plt.show()

    result = pd.DataFrame([x0.values, x1.values, ypred]).T
    return result







