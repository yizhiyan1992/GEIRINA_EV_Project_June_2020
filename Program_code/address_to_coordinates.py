from selenium import webdriver
import pandas as pd
import numpy as np
import time

def add_convert_coordi(address):

    url='https://www.google.com/maps'
    driver=webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    input_box=driver.find_element_by_xpath("//*[@id=\"searchboxinput\"]").send_keys(address)
    time.sleep(2)
    click_order=driver.find_element_by_xpath("//*[@id=\"searchbox-searchbutton\"]").click()
    time.sleep(3)
    coordinates_url=driver.current_url
    driver.quit()
    coordinates=coordinates_url.split('@')[1]
    coordinates=coordinates.split(',')
    #print(coordinates)
    #special case
    if len(coordinates)<2:
        lat='None'
        lon='None'
        return [address, lat, lon]
    lat=coordinates[0]
    lon=coordinates[1]
    return [address,lat,lon]

def main():
    File=pd.read_csv(r'C:/Users/Zhiyan/Desktop/Basic_Info2.csv')
    Address=File['Address'].values
    #address = '1044 E Sugarmont Drive, Salt Lake City, UT 84106'
    txt_file=open('C:/Users/Zhiyan/Desktop/coordinates2.txt','w')
    for i in range(len(Address)):
        res=add_convert_coordi(Address[i])
        txt_file.write(','.join(res)+'\n')
        print(i,Address[i],'is successfully processed!')
    txt_file.close()

if __name__=="__main__":
    main()
