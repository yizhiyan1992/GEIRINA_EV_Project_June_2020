from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense,Bidirectional
import numpy as np
import pandas as pd


#####upload data#######################
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
            if i+feature_num-1+target_hop<set_window[1] and len(raw[i+feature_num-1+target_hop:i+feature_num-1+target_hop+3])==3:
                x.append(raw[i:i+feature_num])
                y.append(raw[i+feature_num-1+target_hop:i+feature_num-1+target_hop+3])
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

#decoder input
train_decoder_input=[]
for i in range(train_x.shape[0]):
    train_decoder_input.append([])
    for j in range(train_y.shape[1]):
        if j==0:
            #train_decoder_input[-1].append(train_x[i][-1][0])
            train_decoder_input[-1].append(0)
        else:
            train_decoder_input[-1].append(train_y[i,j-1])
train_decoder_input=np.array(train_decoder_input)
train_y=train_y[:,:,np.newaxis]
train_decoder_input=train_decoder_input[:,:,np.newaxis]
test_y=test_y[:,:,np.newaxis]
'''
train_x=train_x[:,:,np.newaxis]
train_decoder_input=train_decoder_input[:,:,np.newaxis]
test_x=test_x[:,:,np.newaxis]
train_y=train_y[:,:,np.newaxis]
'''
print(train_x.shape,test_x.shape)
print(train_y.shape,test_y.shape)
print(train_decoder_input.shape)

'''
##################################################

        Model Part

###################################################
'''
batch_size=8
epochs=200
latent_dim=128

def Seq2seq_train(encoder_input_data,decoder_input_data,decoder_target_data,epochs,batch_size,test_x,test_y):
    #build encoder
    encoder_inputs=Input(shape=(None,17))
    encoder1 =LSTM(latent_dim,dropout=0.1, return_state=True, return_sequences=True)
    encoder2 = LSTM(latent_dim, dropout=0.1,return_state=True, return_sequences=True)
    encoder=LSTM(latent_dim,dropout=0.1,return_state=True)
    encoder_outputs=encoder1(encoder_inputs)
    encoder_outputs = encoder2(encoder_outputs)
    encoder_outputs,state_h,state_c = encoder(encoder_outputs)
    encoder_status=[state_h,state_c]
    #build decoder
    decoder_input=Input(shape=(None,1))
    decoder_lstm=LSTM(latent_dim,return_sequences=True,return_state=True)
    decoder_outputs, _, _ = decoder_lstm(decoder_input, initial_state=encoder_status)
    decoder_dense = Dense(1)
    decoder_outputs = decoder_dense(decoder_outputs)
    model=Model(inputs=[encoder_inputs,decoder_input],outputs=decoder_outputs)
    #print(model.summary())
    model.compile(optimizer='RMSprop',loss='mae',metrics=['mae'])
    #history=model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
    #      batch_size=16,epochs=epochs,validation_split=0.15)
    #model.save_weights('C:/Users/Zhiyan/Desktop/models/seq2seq/model.h5')
    model.load_weights('C:/Users/Zhiyan/Desktop/models/seq2seq/model_3mon1059.h5')
    import matplotlib.pyplot as plt
    #loss = history.history['loss']
    #val_loss = history.history['val_loss']
    #epochs = range(1, len(loss) + 1)
    #plt.figure()
    #plt.plot(epochs, loss, 'b', label='Training loss')
    #plt.plot(epochs, val_loss, 'r', label='Validation loss')
    #plt.title('T and V loss')
    #plt.legend()
    #plt.show()
    #for i in range(len(epochs)):
    #    print(epochs[i], loss[i], val_loss[i])
    return encoder_inputs,encoder_status,decoder_lstm,decoder_dense

def seq2seq_predict(encoder_inputs,encoder_status,decoder_lstm,decoder_dense):
    encoder_model=Model(encoder_inputs,encoder_status)
    decoder_state_input_h=Input(shape=(latent_dim,))
    decoder_state_input_c=Input(shape=(latent_dim,))
    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
    decoder_inputs = Input(shape=(None, 1))
    decoder_outputs, state_h, state_c = decoder_lstm(
        decoder_inputs, initial_state=decoder_states_inputs)
    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model = Model(
        [decoder_inputs] + decoder_states_inputs,
        [decoder_outputs] + decoder_states)
    return encoder_model,decoder_model

def decode_sequence(input_data,encoder_model,decoder_model):
    res=[]
    states_value=encoder_model.predict(input_data)
    target_seq=np.zeros((1,1,1))
    for i in range(3):
        output, h, c = decoder_model.predict([target_seq] + states_value)
        res.append(int(output[0][0]))
        # Update the target sequence (of length 1).
        target_seq = np.zeros((1,1,1))
        target_seq[0][0][0]=output[0][0]
        target_seq[0, 0, 0] = output
        # Update states
        states_value = [h, c]
    return res


encoder_inputs,encoder_status,decoder_lstm,decoder_dense=Seq2seq_train(train_x,train_decoder_input,train_y,epochs,batch_size,test_x,test_y)
encoder_model,decoder_model=seq2seq_predict(encoder_inputs,encoder_status,decoder_lstm,decoder_dense)

MAE=[]
pre=[]
tru=[]
for seq_index in range(test_x.shape[0]):
    # Take one sequence (part of the training set)
    # for trying out decoding.
    input_seq = test_x[seq_index,:,:]
    input_seq = input_seq[np.newaxis,:,:]
    decoded_seq = decode_sequence(input_seq,encoder_model,decoder_model)
    print('-')
    print('True seq:', test_y[seq_index,:,:].T)
    print('Decoded seq:', decoded_seq)
    for i in range(len(decoded_seq)):
        tru.append(test_y[seq_index][i][0])
        pre.append(decoded_seq[i])
        MAE.append(abs(decoded_seq[i]-test_y[seq_index][i][0]))
print('MAE',np.mean(MAE))
print('MAPE',np.sqrt(np.mean(np.square(MAE))))
tru=np.array(tru)
pre=np.array(pre)
print('R-squared',1-np.sum(np.square(tru-pre))/np.sum(np.square(tru-np.mean(tru))))