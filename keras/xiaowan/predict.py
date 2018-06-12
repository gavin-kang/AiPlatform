#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:jayden 
@file: predict.py 
@time: 2018/06/{DAY} 
"""
from keras.models import load_model
import numpy as np

model=load_model('./model/model.h5')
pre_res=model.predict(np.array([[2.6,3.3,2.9],[3.3,3.4,2.5]]))
print(pre_res)