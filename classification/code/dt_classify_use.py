# -*- coding: utf-8 -*-
from sklearn.externals import joblib  # jbolib模块
import numpy as np
import pandas as pd
from dt_classify_plot import *  # 导入自行编写的混淆矩阵可视化函数


def dt_classify(datapath='../data/test.xls'):

    # datafile = '../data/test.xls'  # 数据名
    data = pd.read_excel(datapath)  # 读取数据，数据的前三列是特征，第四列是标签
    data = data.as_matrix()  # 将表格转换为矩阵取Model

    dt_model = joblib.load('../tmp/tree.pkl')

    # 测试读取后的Model
    yp = dt_model.predict(data[:, :3])

    # 分类器评估
    # 准确率和混淆矩阵可视化
    rate = 100 * score(data[:, 3], yp)  # 准确率
    plot_cm(data[:, 3], yp).show()  # 显示混淆矩阵可视化结果

    # 分类结果
    classify_result = np.c_[data, yp]
    easysee = classify_result[:, [3, 4]]

    # ROC无线图
    plot_roc(data, yp, 'ROC of CART')

    return rate, classify_result

# 测试
dt_classify()
