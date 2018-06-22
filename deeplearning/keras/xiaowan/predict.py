#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:jayden 
@file: predict.py 
@time: 2018/06/{DAY} 
"""
from keras.models import load_model
import numpy as np
import pandas as pd

x_original=pd.read_csv('./data/show_data.csv',encoding='gbk') #读取原始数据
x_predict=x_original.iloc[:,[1,2,3,4,5]].apply(lambda x:(x-np.min(x))/(np.max(x)-np.min(x))).values #切片训练数据
model=load_model('./model/model.h5') #加载模型
pre_res=pd.DataFrame(model.predict(x_predict),columns=['正常','异常']) #预测结果 并且转为dataframe
merge_df=pd.concat([x_original,pre_res],axis=1) #合并原始数据和预测结果
# merge_df.to_csv('./data/predict.csv',encoding="gbk",index=False) #写入文件
print("succeed!")
