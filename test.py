import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

df=pd.read_csv("data/1.csv",usecols=[1,2,3,4,5,6])
min_max_scaled=df.apply(lambda x:(x-np.min(x))/(np.max(x)-np.min(x)))
# min_max_scalad2=(df-df.min())/(df.max()-df.min())
min_max_scaled=df
fig=plt.figure(1)
plt.subplot(231)
plt.hist(min_max_scaled['79'],100)
plt.xlim(0.0,400)
plt.subplot(232)
plt.hist(min_max_scaled['80'])
plt.subplot(233)
plt.hist(min_max_scaled['81'])
plt.subplot(234)
plt.hist(min_max_scaled['227'])
plt.subplot(235)
plt.hist(min_max_scaled['228'])
plt.subplot(236)
plt.hist(min_max_scaled['472'])
plt.xlabel('取值')
plt.ylabel('数量')
plt.show()

sns.set_palette("hls")
mpl.rc("figure", figsize=(9, 5))
data = np.random.randn(200)

