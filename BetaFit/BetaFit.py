# -*- coding:utf-8 -*-
# @Time    : 2018/6/7 17:39
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : BetaFit.py
# @Software: PyCharm

from scipy.optimize import fmin
from scipy.stats import beta
from scipy.special import gamma as gammaf
import matplotlib.pyplot as plt
import numpy as np

#
# # 归一化
# def MaxMinNormalization(x):
#     Min, Max = min(x), max(x)
#     x = (x - Min) / (Max - Min)
#     return x
#
#
# # 随机生成数据(220+-22)
# mu, sigma, sampleNo = 220, 20, 1000
# s = np.random.normal(mu, sigma, sampleNo)
# plt.hist(s, 30, normed=True)
# plt.show()
#
# data = MaxMinNormalization(s)
# a, b, loc, scale = beta.fit(ss)
#
# # plot
# plt.hist(ss, 30, normed=True)
# x = np.linspace(beta.ppf(0.01, a, b),
#                 beta.ppf(0.99, a, b), 1000)
# plt.plot(x, beta.pdf(x, a, b),
#        'r-', lw=2, alpha=0.6, label='beta pdf')
#
# plt.show()


def betaNLL(param,*args):
    '''Negative log likelihood function for beta
    <param>: list for parameters to be fitted.
    <args>: 1-element array containing the sample data.

    Return <nll>: negative log-likelihood to be minimized.
    '''

    a,b=param
    data=args[0]
    pdf=beta.pdf(data,a,b,loc=0,scale=1)
    lg=np.log(pdf)
    #-----Replace -inf with 0s------
    lg=np.where(lg==-np.inf,0,lg)
    nll=-1*np.sum(lg)
    return nll

#-------------------Sample data-------------------
data=beta.rvs(8,4,loc=0,scale=1,size=500)

#----------------Normalize to [0,1]----------------
#data=(data-numpy.min(data))/(numpy.max(data)-numpy.min(data))

#----------------Fit using moments----------------
mean=np.mean(data)
var=np.var(data,ddof=1)
alpha1=mean**2*(1-mean)/var-mean
beta1=alpha1*(1-mean)/mean

#------------------Fit using mle------------------
result=fmin(betaNLL,[1,1],args=(data,))
alpha2,beta2=result

#----------------Fit using beta.fit----------------
alpha3,beta3,xx,yy=beta.fit(data)

print('\n# alpha,beta from moments:',alpha1,beta1)
print('# alpha,beta from mle:',alpha2,beta2)
print('# alpha,beta from beta.fit:',alpha3,beta3)

#-----------------------Plot-----------------------
plt.hist(data,bins=30,normed=True)
fitted = lambda x,a,b:gammaf(a+b)/gammaf(a)/gammaf(b)*x**(a-1)*(1-x)**(b-1) #pdf of beta

xx=np.linspace(0,max(data),len(data))
plt.plot(xx,fitted(xx,alpha1,beta1),'g')
plt.plot(xx,fitted(xx,alpha2,beta2),'b')
plt.plot(xx,fitted(xx,alpha3,beta3),'r')

plt.show()