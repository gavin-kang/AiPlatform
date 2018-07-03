import numpy as np
from scipy import stats
data1 = np.random.normal(loc=3.4,scale=0.1,size=100)
data2 = np.random.normal(loc=3.4,scale=0.1,size=100)
single_value=3.3
# 单样本
test_result = stats.ttest_1samp(data1, single_value)
p_value = test_result[1]

print('p_value:', p_value)
# 双样本
test_result = stats.ttest_ind(data1, data2, equal_var=True)
p_value = test_result[1]
print('p_value:', p_value)
