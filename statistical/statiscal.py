#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@Author:jayden 
@File: statiscal.py 
@Time: 2018/06/21 
"""
import numpy as np
import matplotlib.pyplot as plt
def exponential_smoothing(alpha, data,times=1):
    '''
    指数平滑法预测趋势
    :param alpha: 参数a
    :param data: 需要平滑的序列
    :param times: 平滑次数
    :return:  平滑后的序列
    '''
    data1 = np.zeros(data.shape)
    data1[0] = data[0]
    for i in range(1, len(data1)):
        data1[i] = alpha*data[i]+(1-alpha)*data1[i-1]
    if times==1:
        return data1
    data2 = np.zeros(data.shape)
    data2[0] = data[0]
    for i in range(1, len(data2)):
        data2[i] = alpha*data1[i]+(1-alpha)*data2[i-1]
    data2_a=2*data1-data2
    data2_b=(alpha/(1-alpha)*(data1-data2))
    data2_pre=data2_a+data2_b
    if times==2:
        return data2_pre




s=np.random.randn(100)
s2=exponential_smoothing(0.9,s)
plt.plot(s,label="actual",color='red')
plt.plot(s2,label="pre",color='green')
plt.legend(loc='upper left')
plt.show()