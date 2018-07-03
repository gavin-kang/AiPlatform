import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def mk(x):
    s=0
    length=len(x)
    for m in range(0,length-1):
      for n in range(m+1,length):
          if x[n]>x[m]:
              s=s+1
          elif x[n]==x[m]:
              s=s+0
          else:
              s=s-1
    
    vars=length*(length-1)*(2*length+5)/18
    if s>0:
        zc=(s-1)/math.sqrt(vars)
    elif s==0:
        zc=0
    else:
        zc=(s+1)/math.sqrt(vars)
        
    zc1=abs(zc)
    
    ndash=length*(length-1)//2
    slope1=np.zeros(ndash)
    m=0
    for k in range(0,length-1):
        for j  in range(k+1,length):
            slope1[m]=(x[j]-x[k])/(j-k)
            m=m+1
        
    slope=np.median(slope1)
    
    return (slope,zc1)


def CUFK(x):
    sk=0
    length=len(x)
    list = []
    list.append(0.0)
    #print("ufk: 0.0")
    for i in range(2, length):
        for j in range(1, i):
            if x[i]>x[j]:
                sk+=1
            else:
                sk+=0
        esk=float(i*(i-1.0)/4.0)
        varsk=float(i*(i-1.0)*(2.0*i+5.0)/72.0)
        ufk=(sk-esk)/math.sqrt(varsk)
        #print("ufk: ",ufk)
        list.append(ufk)

    return list

def CUBK(x):
    sk=0
    length=len(x)
    list = []
    for i in range(1, length):
        x[i]=x[length-i]

    for i in range(2, length):
        for j in range(1,i):
            if x[i]>x[j]:
                sk+=1
            else:
                sk+=0
        esk=float(i*(i-1.0)/4.0)
        varsk=float(i*(i-1.0)*(2.0*i+5.0)/72.0)
        ubk=0-(sk-esk)/math.sqrt(varsk)
        
        list.append(ubk)
        #print("ubk", ubk)

    return list

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

def LoadCSVData(path):
    list=[]
    data = pd.read_csv(path)
    for index,row in data.iterrows():
        if index >= 0 and index < 30:
            #print(row['1'])
            list.append(row['1'])

    return list

def WriteCSVData(list, path):
    data = pd.DataFrame(list)
    data.to_csv(path,index=False,sep=',')

def show_data(list_actual_value, sp_list):
    plt.figure(figsize=(14, 6), dpi=80)
    plt.plot(list_actual_value, color='blue', label="actual value")
    plt.plot(sp_list,color='red',label="predictive value")    
    # plt.legend(loc='lower right')
    plt.legend(bbox_to_anchor=[0.3, 1])
    plt.title('Projects')
    plt.ylabel('number')
    plt.show()

list_data=LoadCSVData('./data/show_data.csv')

(slope,zc1)=mk(list_data)
list_ufk=CUFK(list_data)
list_ubk=CUBK(list_data)

print("斜率: ", slope)
print("统计检验量: ", zc1)

plt.figure(figsize=(14, 6), dpi=80)
plt.plot(list_ubk,'r', label='ubk')
plt.plot(list_ufk,'b',label='ufk')
plt.legend(bbox_to_anchor=[0.3, 1])
plt.title("Sen's & Mann-Kendall")
# plt.legend(loc='lower right')
plt.grid()  
plt.show()

sp_list = es(list_data)
# WriteCSVData(sp_list, "projects/AiPlatform/sens_mann-kendall/data/data_sp.csv")
show_data(list_data, sp_list)

