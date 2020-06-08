import numpy as np
import pandas as pd
import os

'''
For each EV location, the following information need to be captured (some of them may miss):
1. Location ID
2. Name
3. Address
4. Rating
5. Opening hours
6. Phone Number
7. Parking info
8. Amenities
9. Description
10. Historical total check-ins
11. Power Level
12. The total number of stations
13. Charger Type
'''
def process_one_location(File_path,File_name):

    loc=open(os.path.join(File_path,File_name))
    loc_info=loc.readlines()
    Info_array=[[] for _ in range(13)]
    ID=File_name.split('_')[-1][:-4]
    Info_array[0].append(ID)

    for row in loc_info:
        row_info=row.split('#')
        # processing name
        #print(row_info)
        if row_info[0]=='Name':
            Info_array[1].append(row_info[1])
        elif row_info[0]=='Location':
            Info_array[2].append(row_info[1])
        elif row_info[0]=='Rating':
            Info_array[3].append(row_info[1])
        elif row_info[0]=='OpeningTime':
            Info_array[4].append(row_info[1])
        elif row_info[0]=='Parking':
            Info_array[5].append(row_info[1])
        elif row_info[0]=='PhoneNumber':
            Info_array[6].append(row_info[1])
        elif row_info[0] == 'Amenities':
            Info_array[7].append(row_info[1])
        elif row_info[0] == 'Description':
            Info_array[8].append(row_info[1])
        elif row_info[0] == 'CheckinTimes':
            res=row_info[1].split('(')
            res=res[1].split(')')[0]
            Info_array[9].append(res)
        elif row_info[0] == 'PowerLevel':
            Info_array[10].append(row_info[1])
        elif row_info[0]=='PlugType':
            temp=row_info[1].split()
            for t in temp:
                if t.isnumeric():
                    num_of_station=t
                if t=='Station' or t=='Stations':
                    break
            if Info_array[11]==[]:
                Info_array[11].append(num_of_station)
            else:
                Info_array[11][0]=str(int(Info_array[11][0])+int(num_of_station))
        elif row_info[0]=='PlugTypeSummary':
            Info_array[12].append(row_info[1])
    print(ID, ' has been successfully processed.')
    return np.array(Info_array).T

def main():
    File_name = r'Basic_info_ID_8663.txt'
    File_path = r'C:/Users/Zhiyan/Desktop/Utah/BasicInfo/'
    Save_file=r'C:/Users/Zhiyan/Desktop/Basic_Info.csv'
    Locations=os.listdir(File_path)
    print('The total number of charging stations: ',len(Locations))

    for i in range(len(Locations)):
        temp=process_one_location(File_path, Locations[i])
        if i==0:
            Locations_export=temp
        else:
            Locations_export=np.concatenate((Locations_export,temp))
    print(Locations_export.shape)
    Locations_export = pd.DataFrame(np.array(Locations_export),columns=['ID', 'Name', 'Address', 'Rating', 'OpeningHour', 'PhoneNum', 'Parking',
                                      'Amenities','Description', 'TotalCheckins', 'PowerLevel', 'NumofStation', 'ChargeType'])
    Locations_export.to_csv(Save_file)

if __name__=='__main__':
    main()
