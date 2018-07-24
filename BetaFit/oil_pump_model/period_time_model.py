# -*- coding:utf-8 -*-
# @Time    : 2018/6/22 16:31
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : period_time_model.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import datetime
from operating_condition_classify import oc_clasf

start_time = datetime.datetime.now()

total_data = pd.read_csv('./data/20180620.csv', header=None)
new_data = oc_clasf(total_data)
data_0 = pd.DataFrame(new_data[new_data[2] == 0].values)
data_1 = pd.DataFrame(new_data[new_data[2] == 1].values)

q = 200
plt.figure()
plt.subplot(211)
plt.plot(data_0[1][:q])
plt.subplot(212)
plt.plot(data_1[1][:q])
plt.show()


# 把data_0替换为输入变量
def change_count(data):
    time = []
    for i in range(len(data)-2):
        tmp1 = float(data[1][i+1] - data[1][i])
        tmp2 = float(data_0[1][i+2] - data_0[1][i+1])
        if tmp1 > 0 and tmp2 < 0:
            if data[1][i+1] > 6.15:
                if i < 10:
                    time += [data[0][i], ] + [data[0][i+1], ]  # 注意顺序
                else:
                    ls = [data[1][i-3], data[1][i-2], data[1][i-1], data[1][i], data[1][i+1]]
                    lss = pd.Series(ls, index=[i-3, i-2, i-1, i, i+1])
                    min_index = lss[lss == min(lss)].index
                    time += list(data[0][min_index].values) + [data[0][i+1], ]
    return time


def date_gap(date):
    result = []
    for j in range(1, len(date)):
        d0 = datetime.datetime.strptime(date[j-1], '%Y/%m/%d %H:%M')
        d1 = datetime.datetime.strptime(date[j], '%Y/%m/%d %H:%M')
        tmp = d1 - d0
        result.append(tmp.seconds)
    return result


# main,时间间隔以秒为单位
time0 = change_count(data_0)
gap0 = pd.Series(date_gap(time0))/60
time1 = change_count(data_1)
gap1 = pd.Series(date_gap(time1))/60

end_time = datetime.datetime.now()
print('程序运行时间：%d s' % (end_time - start_time).seconds)


# gap0.to_csv('./data/gap0.csv', encoding='utf-8', index=False)
# gap1.to_csv('./data/gap1.csv', encoding='utf-8', index=False)



