import numpy as np
import pandas as pd


#####upload data
seriesUT=pd.read_csv('C:/Users/Zhiyan/Desktop/UT_time_series_daily.csv', header=0)
clusterUT=['Cluster1','Cluster2','Cluster3','Cluster4','Cluster5','Cluster6','Cluster7','Cluster8','Cluster9']
GeofeatureUT=pd.read_csv('C:/Users/Zhiyan/Desktop/UT_Geofeature.csv', header=0,index_col=0)
print(GeofeatureUT)
seriesLA=pd.read_csv('C:/Users/Zhiyan/Desktop/LA_time_series_daily.csv', header=0)
clusterLA=['Cluster1','Cluster2','Cluster3','Cluster4','Cluster5','Cluster6','Cluster7']
GeofeatureLA=pd.read_csv('C:/Users/Zhiyan/Desktop/LA_Geofeature.csv', header=0,index_col=0)
#split train/vali/test, train:2016-2017 vali: 2018 test: 2019-2020 Feb
train_idx=[0,1097]
vali_idx=[1097,1300]
test_idx=[1300,1521]

def create_feature_and_label(series,cluster,feature_num,target_hop,set_window,Geofeature):
    '''
    :param series: raw data
    :param feature_num: the number of historical months used for prediction
    :param target_hop: which month we want to predict for future staring from current time step
    :set_window: the range for each set
    :return:
    '''
    x = []
    y = []

    DayofWeek=pd.get_dummies(series['Weekend']).values
    Date = []
    Geo= []
    for c in range(len(cluster)):
        raw=series[cluster[c]].values
        for i in range(set_window[0],set_window[1]):
            # to guarantee the x and y are in the limited range
            if i+feature_num+target_hop<set_window[1]:
                #if np.sum(raw[i:i+feature_num])!=0 and raw[i+feature_num+1]!=0:
                x.append(raw[i:i+feature_num])
                y.append(raw[i+feature_num+target_hop])
                Date.append(DayofWeek[i+feature_num+target_hop])
                Geo.append(np.array([Geofeature.loc[cluster[c],'No_Stations'],Geofeature.loc[cluster[c],'Level1'],Geofeature.loc[cluster[c],'Level2'],Geofeature.loc[cluster[c],'Level3'],Geofeature.loc[cluster[c],'Tesla'],
                                     Geofeature.loc[cluster[c],'Visits'],Geofeature.loc[cluster[c],'Open_24'],Geofeature.loc[cluster[c],'Open_not24'],Geofeature.loc[cluster[c],'Open_unknown'],
                                     Geofeature.loc[cluster[c], 'Park_free'], Geofeature.loc[cluster[c], 'Park_pay'],Geofeature.loc[cluster[c], 'Park_unknown']]))
                #Geo.append(np.array([Geofeature.loc[cluster[c],'Open_24'],Geofeature.loc[cluster[c],'Open_not24'],Geofeature.loc[cluster[c],'Open_unknown']]))
                #Geo.append(np.array([Geofeature.loc[cluster[c], 'Park_free'], Geofeature.loc[cluster[c], 'Park_pay'],Geofeature.loc[cluster[c], 'Park_unknown']]))
    x=np.array(x)
    y=np.array(y)
    Geo=np.array(Geo)
    Geo=Geo/np.max(Geo,axis=0)
    Date=np.array(Date)
    x=np.column_stack((x,Date,Geo))
    return x,y

def merge(cities_x,cities_y):
    for i in range(len(cities_x)):
        if i==0:
            Concat_x=cities_x[i]
            Concat_y=cities_y[i]
        else:
            Concat_x=np.concatenate([Concat_x,cities_x[i]])
            Concat_y=np.concatenate([Concat_y,cities_y[i]])
    #shuffle
    order=np.random.permutation(range(Concat_y.shape[0]))
    Concat_x=Concat_x[order,:]
    Concat_y=Concat_y[order]
    return Concat_x,Concat_y

# transfer the time-series data into features and labels
train_x_UT,train_y_UT=create_feature_and_label(seriesUT,clusterUT,3,1,train_idx,GeofeatureUT)
train_x_LA,train_y_LA=create_feature_and_label(seriesLA,clusterLA,3,1,train_idx,GeofeatureLA)
vali_x_UT,vali_y_UT=create_feature_and_label(seriesUT,clusterUT,3,1,vali_idx,GeofeatureUT)
vali_x_LA,vali_y_LA=create_feature_and_label(seriesLA,clusterLA,3,1,vali_idx,GeofeatureLA)
test_x_UT,test_y_UT=create_feature_and_label(seriesUT,clusterUT,3,1,test_idx,GeofeatureUT)
test_x_LA,test_y_LA=create_feature_and_label(seriesLA,clusterLA,3,1,test_idx,GeofeatureLA)

#merge data from different regions and randomly shuffle
train_cities_x=[train_x_UT,train_x_LA]
train_cities_y=[train_y_UT,train_y_LA]
train_x,train_y=merge(train_cities_x,train_cities_y)
vali_cities_x=[vali_x_UT,vali_x_LA]
vali_cities_y=[vali_y_UT,vali_y_LA]
vali_x,vali_y=merge(vali_cities_x,vali_cities_y)
test_cities_x=[test_x_UT,test_x_LA]
test_cities_y=[test_y_UT,test_y_LA]
test_x,test_y=merge(test_cities_x,test_cities_y)
print(train_x.shape,vali_x.shape,test_x.shape)

#model training
def MAE(true_val,pred_val):
    return np.mean(np.abs(true_val-pred_val))

def MSE(true_val,pred_val):
    return np.mean(np.square(true_val-pred_val))

import xgboost as xgb
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
params = {'n_estimators': 400, 'learning_rate': 0.1}
model=xgb.XGBRegressor(**params)
#model=RandomForestRegressor(n_estimators=100)
#model=MLPRegressor()
model.fit(train_x,train_y)
print(model.score(train_x,train_y))
print(model.score(vali_x,vali_y))
print(model.score(test_x,test_y))
pred_val=model.predict(test_x)
pred_val=pred_val.astype('int')
print(MAE(test_y,pred_val))
print(MSE(test_y,pred_val))
for i in range(100):
    print(test_y[i],pred_val[i])