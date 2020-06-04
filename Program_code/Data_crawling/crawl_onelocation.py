from selenium import webdriver
from bs4 import BeautifulSoup
import time

station_ID='8663'
start_time=time.time()
driver = webdriver.Chrome()
driver.get('https://www.plugshare.com/location/'+station_ID)
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
f=open(r"C:/Users/Zhiyan/Desktop/Basic_info_ID_"+station_ID+".txt",'w')
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
#total checkin times
checkin=driver.find_element_by_xpath("//*[@id=\"checkins\"]/div[1]")
f.write('CheckinTimes#'+checkin.text+'#\n')
time.sleep(0.5)
#type of plugs
'''
target= driver.find_element_by_xpath("//*[@id=\"connectors\"]/div[3]")
driver.execute_script("arguments[0].scrollIntoView();",target)
time.sleep(1)
Type=driver.find_elements_by_class_name("connector.ng-scope")
for t in Type:
    print(t.text)
    f.write('PlugType#'+t.text+'#\n')
time.sleep(0.5)
'''
PlugT=driver.find_element_by_xpath("//*[@id=\"ports\"]/div[1]")
f.write('PlugType#'+PlugT.text+'#\n')
time.sleep(0.5)
f.close()

###############crawl the historical visits############################
#scroll down
target = driver.find_element_by_xpath("//*[@id=\"checkins\"]/div[2]/span[3]")
driver.execute_script("arguments[0].scrollIntoView();", target)
time.sleep(1)

ele_fromcity = driver.find_element_by_xpath("//*[@id=\"checkins\"]/div[2]/span[3]")
time.sleep(2)
ele_fromcity.click()

content = driver.page_source.encode('utf-8')
bf1=BeautifulSoup(content,'lxml')
result=bf1.find_all(class_='date ng-binding')

output=open(r'C:/Users/Zhiyan/Desktop/Visit_ID_'+station_ID+'.txt','w')
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
