from dateutil.parser import parse
import numpy as np
import pandas as pd
import os

def add_time(time_list,file_name):
    f=open(r'C:/Users/Zhiyan/Desktop/Utah/HistoricReview/'+file_name,encoding='utf-8')
    lines=f.readlines()
    if len(lines)==0:
        return time_list
    for i in range(len(lines)):
        if len(lines[i].split('#'))>2 and lines[i].split('#')[1]=='Charger':
            time_list.append(parse(lines[i+1]))
    f.close()
    return time_list

def implement_matrix(file_name,Date_matrix):
    f = open(r'C:/Users/Zhiyan/Desktop/Utah/HistoricReview/' + file_name, encoding='utf-8')
    station_ID=file_name.split('_')[-1][:-4]
    lines = f.readlines()
    for i in range(len(lines)):
        if len(lines[i].split('#'))>2 and lines[i].split('#')[1]=='Charger':
            Date_matrix.loc[parse(lines[i+1]),station_ID]+=1
    f.close()

def main():
    files=os.listdir(r'C:/Users/Zhiyan/Desktop/Utah/HistoricReview/')
    time_list=[]
    station_list=[]
    for i in range(len(files)):
        station_list.append(files[i].split('_')[-1][:-4])
        time_list=add_time(time_list,files[i])

    time_list.sort()
    print('the number of stations',len(station_list))
    print('total records',len(time_list))
    print('earliest time:',time_list[0])
    print('latest time:',time_list[-1])

    date_range=pd.date_range(start=time_list[0],end=time_list[-1])
    print(type(date_range))
    print(len(date_range))
    Date_matrix=pd.DataFrame(np.zeros((len(date_range),len(station_list))),index=date_range,columns=station_list)
    for i in range(len(files)):
        implement_matrix(files[i],Date_matrix)
    Date_matrix.to_csv(r'C:/Users/Zhiyan/Desktop/Date_matrix.csv')

if __name__=='__main__':
    main()
