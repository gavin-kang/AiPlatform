# -*- coding:utf-8 -*-
# @Time    : 2018/6/12 17:38
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : yuzhi_value.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import random

show_data = pd.read_csv('./show_data.csv', header=None)

both = show_data[:99]
minmax = pd.DataFrame(np.random.randn(1, 2))
minmax.drop(0, inplace=True)
for j in range(1, 6):
    amin1 = min(both.iloc[:, j])
    amax1 = max(both.iloc[:, j])
    minmax = minmax.append(pd.DataFrame([[amin1, amax1], ]))


def yuzhi(j, a, b):

    def rand(p):
        return random.uniform(0, p)

    def loc(j):
        loc1 = float(minmax.iloc[j, 0]) - rand(a)
        loc2 = float(minmax.iloc[j, 1]) + rand(b)
        return list([loc1, loc2])

    yuzhi = pd.DataFrame(np.random.randn(1, 2))
    yuzhi.drop(0, inplace=True)

    for i in range(200):
        yuzhi = yuzhi.append(pd.DataFrame([loc(j)],))
    return yuzhi


yuzhi1 = yuzhi(0, 2, 2)
yuzhi2 = yuzhi(1, 2, 2)
yuzhi3 = yuzhi(2, 2, 2)
yuzhi4 = yuzhi(3, 0.01, 0.01)
yuzhi5 = yuzhi(4, 0.01, 20)

yuzhi = pd.concat([yuzhi1, yuzhi2, yuzhi3, yuzhi4, yuzhi5], axis=1)

# yuzhi.to_csv('BetaFit/yuzhi_value.csv', encoding='utf-8', index=False)
