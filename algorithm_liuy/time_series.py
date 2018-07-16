# -*- coding:utf-8 -*-
# @Time    : 2018/7/11 15:18
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : ts_arima.py
# @Software: PyCharm
# arima时序模型

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import style
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.stats.diagnostic import acorr_ljungbox  # 白噪声检验
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.tsa.api as smt
import seaborn as sns
style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# 对原始数据进行ACF、PACF检验
def tsplot(y, lags=None, title='', figsize=(14, 8)):
    fig = plt.figure(figsize=figsize)
    layout = (2, 2)
    ts_ax = plt.subplot2grid(layout, (0, 0))
    hist_ax = plt.subplot2grid(layout, (0, 1))
    acf_ax = plt.subplot2grid(layout, (1, 0))
    pacf_ax = plt.subplot2grid(layout, (1, 1))

    y.plot(ax=ts_ax)
    ts_ax.set_title(title)
    y.plot(ax=hist_ax, kind='hist', bins=25)
    hist_ax.set_title('Histogram')
    smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
    smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
    [ax.set_xlim(0) for ax in [acf_ax, pacf_ax]]
    sns.despine()
    fig.tight_layout()
    plt.show()
    return ts_ax, acf_ax, pacf_ax


# 平稳性检测(P值大于0.05，则存在单位根，是不平稳时间序列）
# adf_jy返回值依次为adf、pvalue、usedlag、nobs、critical values、icbest、regresults、resstore
def steady(sdata):
    adf_jy = ADF(sdata)  # data[u'销量']
    adf_p_value = adf_jy[1]
    return adf_jy, adf_p_value


# 白噪声检验
def w_noise(wdata):
    w_noise = acorr_ljungbox(wdata, lags=1)  # 返回统计量和p值
    w_p_value = float(w_noise[1])
    return w_noise, w_p_value


# 差分后的结果（如果不平稳）
def ts_diff(ddata):
    D_data = ddata.diff().dropna()  # dropna是缺失值处理
    D_data.columns = [u'1阶差分']
    return D_data


def ts_arima(tsdata, forenum=5):
    tsdata = tsdata.astype(float)
    # 定阶
    D_data = ts_diff(tsdata)
    pmax = int(len(D_data) / 10)  # 一般阶数不超过length/10
    qmax = int(len(D_data) / 10)  # 一般阶数不超过length/10
    bic_matrix = []  # bic矩阵
    for p in range(pmax + 1):
        tmp = []
        for q in range(qmax + 1):
            try:  # 存在部分报错，所以用try来跳过报错。
                tmp.append(ARIMA(tsdata, (p, 1, q)).fit().bic)
            except:
                tmp.append(None)
        bic_matrix.append(tmp)

    bic_matrix = pd.DataFrame(bic_matrix)  # 从中可以找出最小值

    # 可视化BIC矩阵
    fig, ax = plt.subplots(figsize=(10, 8))
    ax = sns.heatmap(bic_matrix,
                     mask=bic_matrix.isnull(),
                     ax=ax,
                     annot=True,
                     fmt='.2f',
                     )
    ax.set_title('BIC')
    plt.show()

    p, q = bic_matrix.stack().idxmin()  # 先用stack展平，然后用idxmin找出最小值位置。
    # print(u'BIC最小的p值和q值为：%s、%s' % (p, q))

    model = ARIMA(tsdata, (p, 1, q)).fit()  # 建立ARIMA(0, 1, 1)模型
    summary = model.summary2()  # 给出一份模型报告
    forecast = model.forecast(forenum)  # 作为期forenum天的预测，返回预测结果、标准误差、置信区间。
    return bic_matrix, p, q, model, summary, forecast


# 测试
# 读取数据
discfile = '../data/arima_data.xls'
forecastnum = 5
data = pd.read_excel(discfile, index_col=u'日期')
ddata = data[u'销量']
# 检验
ts_ap = tsplot(ddata, title='A Given Training Series', lags=20)  # ACF 和 PACF 检验
s_total, s_p = steady(ddata)  # 平稳性检验
w_total, w_p = w_noise(ddata)
# 差分
dif_data = ts_diff(ddata)
# arima模型
bic_matrix1, p1, q1, model1, summary, forecast = ts_arima(ddata)
