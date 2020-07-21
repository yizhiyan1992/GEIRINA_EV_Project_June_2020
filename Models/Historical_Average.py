from pandas import read_csv
from pandas import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import numpy as np

series=read_csv('C:/Users/Zhiyan/Desktop/UT_time_series.csv', header=0)
cluster=['Cluster1','Cluster2','Cluster3','Cluster4','Cluster5','Cluster6','Cluster7','Cluster8','Cluster9']
f=open(r'C:/Users/Zhiyan/Desktop/HistoricalAverage_UT.txt','w')
#the index in 2016,2017,2018,2019
P_idx=[[6,18,30],[7,19,31],[8,20,32],[9,21,33],[10,22,34],[11,23,35],[0,12,24,36],[1,13,25,37]]
for c in range(len(cluster)):
    X=series[cluster[c]].values
    Date = series['Date'].values
    predictions = list()
    for i in range(len(Date)):
        if i%6!=0:
            Date[i]=''

    for i in range(len(P_idx)):
        p_val=int(np.average([X[k] for k in P_idx[i]]))
        f.write(str(cluster[c])+','+str(p_val)+'\n')
        predictions.append(p_val)
    print(predictions)
    predictions=list(X[36:42])+predictions
    plt.plot(range(len(predictions)),predictions,'r--',label='predicted')
    plt.plot(range(len(X[36:])),X[36:],'b-',label='actual')
    plt.xlabel('Time')
    plt.ylabel('Charging Demand')
    plt.title('Charging Demand Prediction by HA (Los Angeles)')
    plt.xticks(range(len(Date[36:])),Date[36:])
f.close()
plt.savefig(r'C:/Users/zhiyan/desktop/HA_LA_case.png',dpi=300)
plt.show()
