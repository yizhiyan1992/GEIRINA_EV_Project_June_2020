from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def crawl_one_location(url,path1,ID,counter):
    start_time=time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)


    #close the welcome-window interface
    # name of location

    f=open(path1 + 'EV_location' + str(counter)+".txt", 'w', encoding='utf-8')
    f.write('StationID#' + str(ID) + '#\n')
    now = time.localtime((time.time()))
    local_time = time.strftime('%Y-%m-%d %H:%M:%S',now)
    f.write('Accessed_time#'+str(local_time)+'#\n')
    name=driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]')
    time.sleep(1)
    f.write('Name#' + name.text + '#\n')
    name = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[10]/button/div[1]')
    time.sleep(1)
    f.write('Address#' + name.text + '#\n')
    i=2
    while True:
        try :
            name = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[7]/div['+str(i)+']/div/div[1]')
            time.sleep(1)
            f.write('Info#' + name.text + '#\n')
            i+=1
        except:
            print('end')
            break

    f.close()
    driver.quit()

def main():
    f=pd.read_csv(r'C:/Users/Zhiyan/Desktop/location.csv')
    url_list=list(f['location'].values)
    ID=list(f['ID'].values)
    print(len(url_list))
    path1=r'C:/Users/Zhiyan/Desktop/Chargepoint/Location/'
    counter=0
    time_A=time.time()
    for i in range(len(url_list)):
        crawl_one_location(url_list[i],path1,ID[i],counter)
        counter+=1
    time_B=time.time()
    print((time_B-time_A)/60)
if __name__=='__main__':
    main()
