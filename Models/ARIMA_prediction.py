from pandas import read_csv
from pandas import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA

series=read_csv('C:/Users/Zhiyan/Desktop/LA_time_series.csv', header=0)
cluster=['Cluster1','Cluster2','Cluster3','Cluster4','Cluster5','Cluster6','Cluster7']

f=open(r'C:/Users/Zhiyan/Desktop/ARIMA_LA666.txt','w')
for c in range(len(cluster)):
    X = series[cluster[c]].values
    Date=series['Date'].values
    for i in range(len(Date)):
        if i%6!=0:
            Date[i]=''
    train, test = X[0:45], X[45:]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        print(cluster[c])
        if cluster[c]=='Cluster6':
            model = ARIMA(history, order=(1, 1, 0))
        else:
            model = ARIMA(history, order=(1,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(yhat)
        print(history)
        print('cluster=%s,predicted=%f, expected=%f' % (cluster[c],yhat, obs))
        f.write(str(cluster[c])+','+str(int(obs))+','+str(int(yhat))+'\n')
    predictions=list(train[36:])+predictions
    plt.plot(range(len(predictions)),predictions,'r--',label='predicted')
    plt.plot(range(len(X[36:])),X[36:],'b-',label='actual')
    plt.xlabel('Time')
    plt.ylabel('Charging Demand')
    plt.title('Charging Demand Prediction by ARIMA (the State of Utah)')
    plt.xticks(range(len(Date[36:])),Date[36:])

f.close()
plt.savefig(r'C:/Users/zhiyan/desktop/ARIMA_case.png')
plt.show()
