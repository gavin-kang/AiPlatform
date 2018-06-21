#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:jayden 
@file: PCA.py 
@time: 2018/06/16
"""

from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import pandas as pd

data_arr=pd.read_csv('../data/data.csv',usecols=[0,1,2,3],dtype=float)
#数据标准化 数据范围（-1，1）
std_scaler=StandardScaler()
std_scaler.fit(data_arr)
#归一化 数据范围（0，1）
min_max_scaler=MinMaxScaler()
min_max_scaler.fit(data_arr)
data_tra=min_max_scaler.transform(data_arr)
data_std=std_scaler.transform(data_arr)

#主成分分析 达到降维和可视化作用
pca=PCA(n_components=0.95,svd_solver='full')
pca.fit(data_tra)
min_max_pac=pca.transform(data_tra)
std_pca=pca.transform(data_std)
print(pca.explained_variance_ratio_)