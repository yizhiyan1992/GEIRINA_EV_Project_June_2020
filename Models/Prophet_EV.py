import pandas as pd
import numpy as np
from fbprophet import Prophet
import matplotlib.pyplot as plt
import datetime

dataUT=pd.read_csv('C:/Users/Zhiyan/Desktop/UT_time_series.csv')
ClustersUT=[dataUT.Cluster1,dataUT.Cluster2,dataUT.Cluster3,dataUT.Cluster4,dataUT.Cluster5,
          dataUT.Cluster6,dataUT.Cluster7,dataUT.Cluster8,dataUT.Cluster9]
dataLA=pd.read_csv('C:/Users/Zhiyan/Desktop/LA_time_series.csv')
ClustersLA=[dataLA.Cluster1,dataLA.Cluster2,dataLA.Cluster3,dataLA.Cluster4,dataLA.Cluster5,
          dataLA.Cluster6,dataLA.Cluster7]

data=[dataUT,dataLA]
Clusters=[ClustersUT,ClustersLA]
'''
holidays = pd.DataFrame({
  'holiday': 'holiday',
  'ds': pd.to_datetime(['2016-01-01','2016-01-18','2016-02-15','2016-05-30','2016-07-04',
                        '2016-09-05','2016-10-10','2016-11-11','2016-11-24','2016-12-26',
                        '2017-01-01','2017-01-16','2017-02-20','2017-05-29','2017-07-04',
                        '2017-09-04','2017-10-09','2017-11-10','2017-11-23','2017-12-25',
                        '2018-01-01','2018-01-15','2018-02-19','2018-05-28','2018-07-04',
                        '2018-09-03','2018-10-08','2018-11-12','2018-11-22','2018-12-25',
                        '2019-01-01','2019-01-21','2019-02-18','2019-05-27','2019-07-04',
                        '2019-10-14', '2019-11-11', '2019-11-28', '2019-12-25',
                        '2020-01-01', '2020-01-20', '2020-02-17'])})
'''
holidays = pd.DataFrame({
  'holiday': 'holiday',
  'ds': pd.to_datetime(['2016-01-01','2016-02-1','2016-05-1','2016-07-1',
                        '2016-09-1','2016-10-1','2016-11-1','2016-12-1',
                        '2017-01-01','2017-02-1','2017-05-1','2017-07-1',
                        '2017-09-01','2017-10-01','2017-11-10','2017-12-01',
                        '2018-01-01','2018-02-01','2018-05-01','2018-07-01',
                        '2018-09-01','2018-10-01','2018-11-01','2018-12-01',
                        '2019-01-01','2019-02-01','2019-05-01','2019-07-01',
                        '2019-10-01', '2019-11-01', '2019-12-01',
                        '2020-01-01', '2020-02-01'])})
MAE=[]
for d in range(2):
    for c in range(len(Clusters[d])):
        arr=np.array([data[d].Date.values[:-5],Clusters[d][c].values[:-5]])
        df=pd.DataFrame(arr.T,columns=['ds','y'])
        df['ds']=pd.to_datetime(df['ds'])

        m=Prophet(changepoint_prior_scale=0.005,holidays=holidays,holidays_prior_scale =1)
        m.fit(df)
        future=m.make_future_dataframe(periods=5,freq='M')
        future['ds']=future['ds']+datetime.timedelta(days=1)

        res=m.predict(future)
        m.plot(res)
        plt.show()
        print(res.tail())
        diff=np.abs(res['yhat'].values[45:]-Clusters[d][c].values[45:])
        for val in diff:
            MAE.append(val)
print(MAE)
print(np.mean(MAE))
print(np.sqrt(np.mean(np.square(MAE))))