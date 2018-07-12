#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@Author:jayden 
@File: sta.py
@Time: 2018/06/21 
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def covariance(data):
    '''
    协方差矩阵
    :param data: 数据是numpy的ndarray数组或者pandas的Dataframe格式
    :return:
    '''
    data_frame=pd.DataFrame(data)
    return data_frame.cov()

def correlation(data):
    '''
    相关系数矩阵
    :param data: 数据是numpy的ndarray数组或者pandas的Dataframe格式
    :return:
    '''
    data_frame = pd.DataFrame(data)
    return data_frame.corr()

def full_table_statistics(data):
    '''
    全表统计，返回表中每一列的均值、方差、基础分布等
    :param data: 数据是numpy的ndarray数组或者pandas的Dataframe格式
    :return:
    '''
    data_frame=pd.DataFrame(data)
    return data_frame.describe()



