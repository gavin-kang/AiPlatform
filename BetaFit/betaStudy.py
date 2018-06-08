# -*- coding:utf-8 -*-
# @Time    : 2018/6/7 17:11
# @Author  : yuanjing liu
# @Email   : lauyuanjing@163.com
# @File    : betaStudy.py
# @Software: PyCharm

from scipy.stats import beta
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(1, 1)

# Calculate a few first moments:
a, b = 4, 4
# a, b = 2.31, 0.627
mean, var, skew, kurt = beta.stats(a, b, moments='mvsk')

# Display the probability density function (``pdf``):

x = np.linspace(beta.ppf(0.01, a, b),
                beta.ppf(0.99, a, b), 100)
ax.plot(x, beta.pdf(x, a, b),
       'r-', lw=5, alpha=0.6, label='beta pdf')

# Alternatively, the distribution object can be called (as a function)
# to fix the shape, location and scale parameters. This returns a "frozen"
# RV object holding the given parameters fixed.

# Freeze the distribution and display the frozen ``pdf``:

rv = beta(a, b)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

# Check accuracy of ``cdf`` and ``ppf``:

vals = beta.ppf([0.001, 0.5, 0.999], a, b)
np.allclose([0.001, 0.5, 0.999], beta.cdf(vals, a, b))
# True

# Generate random numbers:

r = beta.rvs(a, b, size=1000)

# And compare the histogram:

ax.hist(r, normed=True, histtype='stepfilled', alpha=0.2)
ax.legend(loc='best', frameon=False)
plt.show()






import numpy as np
from numpy.linalg import cholesky
import matplotlib.pyplot as plt

sampleNo = 1000;
# 一维正态分布
# 下面三种方式是等效的
mu = 3
sigma = 0.1
np.random.seed(0)
s = np.random.normal(mu, sigma, sampleNo )
plt.subplot(141)
plt.hist(s, 30, normed=True)

np.random.seed(0)
s = sigma * np.random.randn(sampleNo ) + mu
plt.subplot(142)
plt.hist(s, 30, normed=True)

np.random.seed(0)
s = sigma * np.random.standard_normal(sampleNo ) + mu
plt.subplot(143)
plt.hist(s, 30, normed=True)

# 二维正态分布
mu = np.array([[1, 5]])
Sigma = np.array([[1, 0.5], [1.5, 3]])
R = cholesky(Sigma)
s = np.dot(np.random.randn(sampleNo, 2), R) + mu
plt.subplot(144)
# 注意绘制的是散点图，而不是直方图
plt.plot(s[:,0],s[:,1],'+')
plt.show()