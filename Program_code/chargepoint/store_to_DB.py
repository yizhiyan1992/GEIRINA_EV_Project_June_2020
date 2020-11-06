import pandas as pd
import numpy as np
import pymysql
import os
"""
fact table:
1. UID
2. Crawl ID
3. Station ID
4. Accessed time
5. Plug Type
6. Power (kw)
7. Total number of port
8. Number of in-use port
"""
def read_txt(path):
    # input: txt file
    # output: a list of detection records
    f=open(path)
    f=f.readlines()
    record=[]
    res=[]
    for idx,line in enumerate(f):
        if line[:3]=='UID':
            record.append(line.split('#')[1])
        if line[:7]=='CrawlID':
            record.append(line.split('#')[1])
        if line[:9]=='StationID':
            record.append(line.split('#')[1])
        if line[:13]=='Accessed_time':
            record.append(line.split('#')[1])
        if line[:5]=='Info#':
            pointer=idx
            recor=0
            while pointer<len(f):
                temp = record.copy()
                temp[0]=temp[0]+'rcor'+str(recor)
                recor+=1
                temp.append(f[pointer].split('#')[1].split('\n')[0])
                pointer+=1
                temp.append(f[pointer].split(' ')[1])
                pointer+=1
                avail=f[pointer].split('#')[0].split(' ')[1].split('/')
                temp.append(avail[1])
                temp.append(int(avail[1])-int(avail[0]))
                pointer+=1
                res.append(temp)
            break
    return res

def insert_records(vals):
    connection = pymysql.connect(host='localhost', user='root', password='YOUR PASSWORD', db='mysql')
    cur = connection.cursor()
    cur.execute("use chargepoint")
    # vals: a list of records
    insert_syntax="""INSERT INTO chargedetect VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur.executemany(insert_syntax,vals)
    connection.commit()
    connection.close()
    return

def main():
    path=r'C:/Users/Zhiyan/Desktop/crawl_record/ADD CRAWL FOLER HERE'
    files=os.listdir(path)
    print(len(files))
    for i in range(len(files)):
        p=os.path.join(path,files[i])
        records=read_txt(p)
        insert_records(records)

if __name__=="__main__":
    main()
