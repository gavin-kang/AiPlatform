#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:jayden 
@file: train.py
@time: 2018/06/{DAY} 
"""

import keras
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.utils import plot_model
import matplotlib.pyplot as plt
import numpy as np
import get_data


num_class=2 #分类数量
epochs=60 #遍历次数
batch_size=128 #批大小

#获取数据集 并且分组
(x_train, y_train), (x_test, y_test)=get_data.load_data(file_path='./data/train_data.csv',y_name='6')
#转换DataFrame对象为张量数组
x_train=x_train.values
y_train=y_train.values
x_test=x_test.values
y_test=y_test.values

print(x_train.shape)


y_train=keras.utils.to_categorical(y_train,2)
y_test=keras.utils.to_categorical(y_test,2)

# 定义神经网络模型的层结构
model=Sequential()
model.add(Dense(5,input_shape=(5,),activation='relu'))
# model.add(Dropout(0.5))
model.add(Dense(num_class,activation='softmax'))

# 指定优化器 损失
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

# 训练模型
history=model.fit(x_train,y_train,batch_size=batch_size,epochs=epochs,verbose=1,validation_split=0.25)

print(history.history.keys())



# 保存模型
model.save('./model/model.h5')

model.save_weights('./model/model_weights.h5')
# plot_model(model)

# 评估模型
acc=model.evaluate(x_test,y_test,verbose=0)
print(acc)

# 解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(1)
# plt.plot(history.history['epoch'],history.history['loss'])
plt.subplot(121)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('模型准确率变化趋势')
plt.ylabel('准确率')
plt.xlabel('训练次数')
plt.legend(['训练', '验证'], loc='upper left')

plt.subplot(122)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('模型误差损失变化趋势')
plt.ylabel('误差损失')
plt.xlabel('训练次数')
plt.legend(['训练', '验证'], loc='lower left')

plt.show()

# fig.savefig('acc.png')