# -*- coding:utf-8 -*-
# @Time    : 2018/6/9 17:39
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : ab_data.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


total_data = pd.read_csv('../BetaFit/minute_data.csv', header=None)
new_data = total_data[4000:6000]
new_data.index = range(len(new_data))

# a1, b1, d1, d2 = BetaModel(new_data.iloc[:, 1])
# a2, b2, d3, d4 = BetaModel(new_data.iloc[:, 3])
min1 = min(new_data.iloc[:, 1])
max1 = max(new_data.iloc[:, 1])
min3 = min(new_data.iloc[:, 3])
max3 = max(new_data.iloc[:, 3])

# 从选取的数据里选择突变点
tb = 1000  # 改变
j = 10  # 改变
jb = list(np.arange(0., 20., 2))  # 改变
eed = len(new_data)
one1 = list((np.ones(len(new_data.iloc[tb+j:eed, 1])))*20)

# 哪一列该百年
new_data.iloc[tb:tb+j, 1] = new_data.iloc[tb:tb+j, 1].add(jb, axis=0)
new_data.iloc[tb+j:eed, 1] = new_data.iloc[tb+j:eed, 1].add(one1, axis=0)
new_data.iloc[tb:tb+j, 3] = new_data.iloc[tb:tb+j, 3].add(jb, axis=0)
new_data.iloc[tb+j:eed, 3] = new_data.iloc[tb+j:eed, 3].add(one1, axis=0)
# 标签
new_data['6'] = 0
new_data.iloc[tb+j:eed, 6] = 1

# 截取前后200数据
show_data = new_data[tb-100:tb+100]

# new_data.to_csv('BetaFit/train_data.csv', encoding='utf-8', index=False)
# show_data.to_csv('BetaFit/show_data.csv', encoding='utf-8', index=False)

data1 = show_data.iloc[:, 1]
data2 = show_data.iloc[:, 2]
data3 = show_data.iloc[:, 3]
data4 = show_data.iloc[:, 4]

plt.figure(1)
plt.subplot(221)
plt.plot(data1)
plt.ylim(0, 100)
plt.subplot(222)
plt.plot(data2)
plt.ylim(0, 100)
plt.subplot(223)
plt.plot(data3)
plt.ylim(0, 100)
plt.subplot(224)
plt.plot(data4)
plt.show()


