# -*- coding:utf-8 -*-
# @Time    : 2018/6/29 18:08
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : chi2_independence.py
# @Software: PyCharm

# 卡方独立性检验
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import chi2

'''
（1）假设检验重要知识
H0:A与B相互独立  H1：A与B不相互独立
若卡方值大于临界值，拒绝原假设，表示A与B不相互独立，A与B相关
函数中re返回为1表示拒绝原假设，0表示接受原假设

（2）参数说明
输入：
alpha --- 置信度，用来确定临界值
data  --- 数据，请使用numpy.array数组
输出：
g     --- 卡方值，也就是统计量
p     --- P值（统计学名词），与置信度对比，也可进行假设检验，P值小于置信度，即可拒绝原假设
dof   --- 自由度
re    --- 判读变量，1表示拒绝原假设，0表示接受原假设
expctd--- 原数据数组同维度的对应理论值

（3）应用场景
要求样本含量应大于40且每个格子中的理论频数不应小于5
'''


def chi2_independence(data, alpha):
    g, p, dof, expctd = chi2_contingency(data)

    if dof == 0:
        print('自由度应该大于等于1')
    elif dof == 1:
        cv = chi2.isf(alpha * 0.5, dof)
    else:
        cv = chi2.isf(alpha * 0.5, dof-1)


    if g > cv:
        re = 1  # 表示拒绝原假设
    else:
        re = 0  # 表示接受原假设

    return g, p, dof, re, expctd


# test
alpha1 = 0.05  # 置信度，常用0.01，0.05，用于确定拒绝域的临界值
data1 = np.array([[442, 514], [38, 6]])
g1, p1, dof1, re1, expctd1 = chi2_independence(alpha1, data1)
