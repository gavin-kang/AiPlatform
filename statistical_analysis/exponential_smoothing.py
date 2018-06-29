import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

def exponential_smoothing(alpha, s):
    s2 = np.zeros(s.shape)
    s2[0] = s[0]
    for i in range(1, len(s2)):
        s2[i] = alpha*s[i]+(1-alpha)*s2[i-1]

    return s2 

def es(list_actual_value):
    alpha = .70
    actual_value_data=np.array(list_actual_value)
    s_single = exponential_smoothing(alpha,actual_value_data)
    s_double = exponential_smoothing(alpha,s_single)
    a_double = 2*s_single-s_double
    b_double = (alpha/(1-alpha))*(s_single-s_double)
    s_pre_double = np.zeros(s_double.shape)
    for i in range(1, len(actual_value_data)):
        s_pre_double[i] = a_double[i-1]+b_double[i-1]

    sp_list = s_pre_double.tolist()
    sp_list.remove(sp_list[0])
    pre_next = a_double[-1]+b_double[-1]*1
    pre_next_two = a_double[-1]+b_double[-1]*2
    sp_list.append(pre_next)
    sp_list.append(pre_next_two)
    return sp_list

def show_data(list_actual_value, sp_list):
    plt.figure(figsize=(14, 6), dpi=80)
    plt.plot(list_actual_value, color='blue', label="actual value")
    plt.plot(sp_list,color='red',label="predictive value")    
    plt.legend(loc='lower right')
    plt.title('Projects')
    plt.ylabel('number')
    plt.show()

def LoadCSVData(path, column):
    list=[]
    data = pd.read_csv(path)
    for index,row in data.iterrows():
        if index >= 0 and index < 200:
            #print(row[column])
            list.append(row[column])
            
    return list

def WriteCSVData(list, path):
    data = pd.DataFrame(list)
    data.to_csv(path,index=False,sep=',')

list_data_1=LoadCSVData('projects/AiPlatform/sens_mann-kendall/data/show_data.csv','1')
sp_list = es(list_data_1)
show_data(list_data_1, sp_list)
