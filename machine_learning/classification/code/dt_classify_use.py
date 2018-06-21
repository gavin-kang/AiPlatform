# -*- coding: utf-8 -*-
from sklearn.externals import joblib  # jbolib模块
import numpy as np
# from dt_classify_plot import *  # 导入自行编写的混淆矩阵可视化函数

# ----------------------------------- 说明 -------------------------------------
# 输入：decline_index --> 电量趋势下降指标
#       loss_index --> 线损指标
#       alarm_index --> 电量趋势下降指标
#
# 输出：yp(判断类别):      0 --> 无窃漏电        1 --> 有窃漏电
#       yp_proba(每个类别的概率) : 第一个位置为0类别的概率，第二个位置为1类别的概率
# ------------------------------------------------------------------------------


def dt_classify(decline_index=4, loss_index=1, alarm_index=3):

    # datafile = '../data/test.xls'  # 数据名
    # data = pd.read_excel(datapath)  # 读取数据，数据的前三列是特征，第四列是标签
    # data = data.as_matrix()  # 将表格转换为矩阵取Model

    dt_model = joblib.load('../tmp/tree_best.pkl')
    # 测试读取后的Model
    data = np.matrix([[decline_index, loss_index, alarm_index]])
    # data = data.as_matrix()
    yp = dt_model.predict(data)
    yp_proba = dt_model.predict_proba(data)
    # # 分类器评估
    # # 准确率和混淆矩阵可视化
    # rate = 100 * score(data[:, 3], yp)  # 准确率
    # plot_cm(data[:, 3], yp).show()  # 显示混淆矩阵可视化结果
    #
    # # 分类结果
    # classify_result = np.c_[data, yp]
    # easysee = classify_result[:, [3, 4]]
    #
    # # ROC线图
    # plot_roc(data, yp, 'ROC of CART')

    return yp,yp_proba

# 测试(5,1,1)、(4,1,3)、(5,1,3)
y, p = dt_classify(4,1,3)
print('判断的类别为：%d' % y)
print('类别0的概率：%f' % p[:, 0])
print('类别1的概率：%f' % p[:, 1])


