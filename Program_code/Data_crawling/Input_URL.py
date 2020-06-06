import pandas as pd
import numpy as np
from crawl_onelocation import crawl_one_location

Utah=pd.read_csv(r'C:/Users/Zhiyan/Desktop/Utah/Utah_location_id.csv')
urls=Utah['URL'].values
crawl_records=open(r'C:/Users/Zhiyan/Desktop/EVrecords.txt','w')
success=pd.read_csv(r'C:/Users/Zhiyan/Desktop/succeed.csv')
success=list(success['ID'].values)
print(len(success))

for i in range(len(urls)):
    station_ID=urls[i].split('/')[-1]
    if int(station_ID) in success:
        print('skip',station_ID,i)
        continue
    url=urls[i]
    path1=r'C:/Users/Zhiyan/Desktop/Utah/BasicInfo'
    path2=r'C:/Users/Zhiyan/Desktop/Utah/HistoricReview'
    crawl_one_location(station_ID,url,path1,path2)
    crawl_records.write(str(i)+','+station_ID+',success!\n')

crawl_records.close()
