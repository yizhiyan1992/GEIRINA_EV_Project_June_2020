import numpy as np
import pandas as pd

file=pd.read_csv(r'C:/Users/Zhiyan/Desktop/Dummy.csv')
ID=file['ID']
Type=file['ChargeType']
Type_list=[]
Type_Dict={}

for idx,t in enumerate(Type):
    chargers=t.split(',')
    for i in range(len(chargers)):
        chargers[i]=chargers[i].strip()
        Type_Dict[chargers[i]]=chargers[i]
    Type_list.append(chargers)

print(Type_Dict.keys())
print(len(Type_Dict))

#detect level
Level=[]

for i in range(len(ID)):
    temp=[0,0,0]
    for j in range(len(Type_list[i])):
        if Type_list[i][j]=='J-1772':
            temp[1]=1
        elif Type_list[i][j]=='CCS/SAE':
            temp[2]=1
        elif Type_list[i][j]=='CHAdeMO':
            temp[2]=1
        elif Type_list[i][j]=='Tesla':
            temp[1]=1
        elif Type_list[i][j]=='Wall':
            temp[0]=1
        elif Type_list[i][j]=='NEMA 14-50':
            temp[1]=1
        elif Type_list[i][j]=='Supercharger':
            temp[2]=1
    Level.append(temp)

# Detect if Tesla only
Tesla_only=[]
for i in range(len(ID)):
    temp=0
    if 'Tesla' in Type_list[i] and len(Type_list[i])==1:
        temp=1
    elif 'Supercharger' in Type_list[i] and len(Type_list[i])==1:
        temp=1
    elif 'Tesla' in Type_list[i] and 'Supercharger' in Type_list[i] and len(Type_list[i])==2:
        temp=1
    Tesla_only.append(temp)

f=open(r'C:/Users/Zhiyan/Desktop/dummy_process_LA.txt','w')
for i in range(len(ID)):
    f.write(str(ID[i])+',')
    for j in Level[i]:
        f.write(str(j)+',')
    f.write(str(Tesla_only[i])+'\n')
f.close()
