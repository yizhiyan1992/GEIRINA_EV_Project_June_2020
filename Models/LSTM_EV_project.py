import numpy as np
import pandas as pd


#####upload data
seriesUT=pd.read_csv('C:/Users/Zhiyan/Desktop/UT_time_series.csv', header=0)
clusterUT=['Cluster1','Cluster2','Cluster3','Cluster4','Cluster5','Cluster6','Cluster7','Cluster8','Cluster9']
GeofeatureUT=pd.read_csv('C:/Users/Zhiyan/Desktop/UT_Geofeature.csv', header=0,index_col=0)
seriesLA=pd.read_csv('C:/Users/Zhiyan/Desktop/LA_time_series.csv', header=0)
clusterLA=['Cluster1','Cluster2','Cluster3','Cluster4','Cluster5','Cluster6','Cluster7']
GeofeatureLA=pd.read_csv('C:/Users/Zhiyan/Desktop/LA_Geofeature.csv', header=0,index_col=0)
#split train/vali/test, train:2016-2017 vali: 2018 test: 2019-2020 Feb
train_idx=[0,42]
vali_idx=[36,42]
test_idx=[42,50]

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
    Geo=[[] for _ in range(16)]
    Geo_dict=['Visits','No_Sites','Open_24','Open_not24','Open_unknown','Park_free','Park_pay','Park_unknown',
              'Level1','Level2','Level3','Tesla','hotel','recreation','service','shopping']
    for c in range(len(cluster)):
        raw=series[cluster[c]].values
        for i in range(set_window[0],set_window[1]):
            # to guarantee the x and y are in the limited range
            if i+feature_num-1+target_hop<set_window[1]:
                x.append(raw[i:i+feature_num])
                y.append(raw[i+feature_num-1+target_hop])
                for d in range(len(Geo)):
                    Geo[d].append([Geofeature.loc[cluster[c], Geo_dict[d]]]*3)


    x=np.array(x)
    y=np.array(y)
    for i in range(len(Geo)):
        Geo[i]=np.array(Geo[i])
        Geo[i]=Geo[i]/np.max(Geo[i],axis=0)

    x=np.stack((x,Geo[0],Geo[1],Geo[2],Geo[3],Geo[4],Geo[5],Geo[6],Geo[7],Geo[8],Geo[9],Geo[10],Geo[11],Geo[12],Geo[13],Geo[14],Geo[15]),axis=2)
    #x=np.column_stack((x))
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
    #Concat_x=Concat_x[:,:,np.newaxis]
    Concat_y=Concat_y[order]
    return Concat_x,Concat_y

# transfer the time-series data into features and labels
train_x_UT,train_y_UT=create_feature_and_label(seriesUT,clusterUT,3,3,train_idx,GeofeatureUT)
train_x_LA,train_y_LA=create_feature_and_label(seriesLA,clusterLA,3,3,train_idx,GeofeatureLA)
vali_x_UT,vali_y_UT=create_feature_and_label(seriesUT,clusterUT,3,3,vali_idx,GeofeatureUT)
vali_x_LA,vali_y_LA=create_feature_and_label(seriesLA,clusterLA,3,3,vali_idx,GeofeatureLA)
test_x_UT,test_y_UT=create_feature_and_label(seriesUT,clusterUT,3,3,test_idx,GeofeatureUT)
test_x_LA,test_y_LA=create_feature_and_label(seriesLA,clusterLA,3,3,test_idx,GeofeatureLA)

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
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

model=Sequential()
model.add(layers.Bidirectional(layers.LSTM(64,return_sequences=True,dropout=0.1),input_shape=(3,17)))
model.add(layers.Bidirectional(layers.LSTM(64,dropout=0.1)))
model.add(layers.Dense(1))
model.compile(optimizer='RMSprop',loss="mae",metrics=['mae'])
history=model.fit(train_x,train_y,batch_size=64,epochs=200,validation_split=0.2)
#model.load_weights('C:/Users/Zhiyan/Desktop/models/LSTM/model941.h5')
loss,acc=model.evaluate(test_x,test_y,steps=1,verbose=0)
#model.save_weights('C:/Users/Zhiyan/Desktop/models/LSTM/model.h5')
y_pre=model.predict(test_x)
test_y=test_y[:,np.newaxis]
print(loss,acc)
print(y_pre.shape)
print(test_y.shape)
print(np.sqrt(np.mean(np.square(test_y-y_pre))))

print(1-np.sum(np.square(y_pre-test_y))/np.sum(np.square(test_y-np.mean(test_y))))

import matplotlib.pyplot as plt
loss=history.history['loss']
val_loss=history.history['val_loss']
epochs=range(1,len(loss)+1)
plt.figure()
plt.plot(epochs,loss,'b',label='Training loss')
plt.plot(epochs,val_loss,'r',label='Validation loss')
plt.title('T and V loss')
plt.legend()
plt.show()

