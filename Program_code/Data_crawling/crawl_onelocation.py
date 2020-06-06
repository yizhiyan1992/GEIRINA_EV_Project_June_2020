from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time

def crawl_one_location(station_ID,url,path1,path2):
    start_time=time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    driver.save_screenshot('C:/Users/Zhiyan/Desktop/5.png')
    #close the welcome-window interface
    close_welcome = driver.find_element_by_xpath("//*[@id=\"optimize-target\"]/md-icon")
    time.sleep(1)
    close_welcome.click()
    #pinpoint the interface
    interface=driver.find_element_by_xpath("//*[@id=\"pane\"]")
    time.sleep(1)

    ###############crawl the basic information of this charging station###
    f=open(path1+"/Basic_info_ID_"+station_ID+".txt",'w',encoding='utf-8')
    #name of location
    name=driver.find_element_by_xpath("//*[@id=\"display-name\"]/div/h1")
    f.write('Name#'+name.text+'#\n')
    time.sleep(0.5)
    #location
    loc=driver.find_element_by_xpath("//*[@id=\"info\"]/div[2]/div[2]/div[2]/a[1]")
    f.write('Location#'+loc.text+'#\n')
    time.sleep(0.5)
    #rating of location
    rating=driver.find_element_by_xpath("//*[@id=\"plugscore\"]")
    f.write('Rating#'+rating.text+'#\n')
    time.sleep(0.5)
    #store hours
    hour=driver.find_element_by_xpath("//*[@id=\"info\"]/div[2]/div[8]/div[2]")
    f.write('OpeningTime#'+hour.text+'#\n')
    time.sleep(0.5)
    #telephone number
    phone=driver.find_element_by_xpath("//*[@id=\"info\"]/div[2]/div[3]/div[2]")
    f.write('PhoneNumber#'+phone.text+'#\n')
    time.sleep(0.5)
    #Parking
    parking=driver.find_element_by_xpath("//*[@id=\"info\"]/div[2]/div[5]/div[2]")
    f.write('Parking#'+parking.text+'#\n')
    time.sleep(0.5)
    #Amenities
    parking=driver.find_element_by_xpath("//*[@id=\"info\"]/div[2]/div[6]/div[2]")
    f.write('Amenities#'+parking.text+'#\n')
    time.sleep(0.5)
    #Description
    Description=driver.find_element_by_xpath("//*[@id=\"info\"]/div[2]/div[9]/div[2]/span")
    f.write('Description#'+Description.text+'#\n')
    time.sleep(0.5)
    #total checkin times
    checkin=driver.find_element_by_xpath("//*[@id=\"checkins\"]/div[1]")
    f.write('CheckinTimes#'+checkin.text+'#\n')
    time.sleep(0.5)
    #plug power level
    powerlevel=driver.find_element_by_xpath("//*[@id=\"ports\"]/div[3]")
    f.write('PowerLevel#'+powerlevel.text+'#\n')
    time.sleep(0.5)
    #type of plugs
    target= driver.find_element_by_xpath("//*[@id=\"connectors\"]/div[3]")
    driver.execute_script("arguments[0].scrollIntoView();",target)
    time.sleep(1)
    Type=driver.find_elements_by_class_name("connector.ng-scope")
    for t in Type:
        f.write('PlugType#'+t.text+'#\n')
    time.sleep(0.5)

    PlugT=driver.find_element_by_xpath("//*[@id=\"ports\"]/div[1]")
    f.write('PlugTypeSummary#'+PlugT.text+'#\n')
    time.sleep(0.5)
    f.close()

    ###############crawl the historical visits############################
    #scroll down
    #target = driver.find_element_by_xpath("//*[@id=\"checkins\"]/div[2]/span[3]")
    #driver.execute_script("arguments[0].scrollIntoView();", target)
    #time.sleep(1)

    if driver.find_element_by_xpath("//*[@id=\"checkins\"]/div[2]/span[3]").is_displayed():
        ele_fromcity = driver.find_element_by_xpath("//*[@id=\"checkins\"]/div[2]/span[3]")
        time.sleep(1)
        ele_fromcity.click()
    content = driver.page_source.encode('utf-8')
    bf1=BeautifulSoup(content,'lxml')
    result=bf1.find_all(class_='date ng-binding')

    output=open(path2+'/Visit_ID_'+station_ID+'.txt','w',encoding='utf-8')
    for i in range(100):
        review = driver.find_elements_by_xpath("//*[@id=\"dialogContent_reviews\"]/div/div/div["+str(i)+"]")
        for tag in review:
            contains=tag.text
            output.write('#Charger#ID'+str(i)+'\n'+contains+'\n')
            status= driver.find_element_by_xpath("//*[@id=\"dialogContent_reviews\"]/div/div/div["+str(i)+"]/div[2]/div[2]/md-icon[1]")
            output.write(status.text)
            cancel_status= driver.find_element_by_xpath("//*[@id=\"dialogContent_reviews\"]/div/div/div["+str(i)+"]/div[2]/div[2]/md-icon[2]")
            output.write(cancel_status.text)
            output.write('\n')
    output.close()
    driver.quit()
    end_time=time.time()
    print('Time consumption: ',end_time-start_time)
    print('Charging station ',station_ID,' has successfully be crawled.')
    return

def main():
    station_ID = '191783'
    url='https://www.plugshare.com/location/191783'
    path1=r'C:/Users/Zhiyan/Desktop/'
    path2 = r'C:/Users/Zhiyan/Desktop/'
    crawl_one_location(station_ID,url,path1,path2)

if __name__=='__main__':
    main()
