from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import smtplib,ssl

def crawl_one_location(url,path1,ID,address,counter):
    start_time=time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    #close the welcome-window interface
    f=open(path1 + 'EV_location' + str(counter)+".txt", 'w', encoding='utf-8')
    f.write('CrawlID#' + str(counter) + '#\n')
    f.write('StationID#' + str(ID) + '#\n')
    f.write('StationURL###' + url + '###\n')
    now = time.localtime((time.time()))
    local_time = time.strftime('%Y-%m-%d %H:%M:%S',now)
    f.write('Accessed_time#'+str(local_time)+'#\n')

    i=2
    while True:
        try :
            name = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[7]/div['+str(i)+']/div/div[1]')
            time.sleep(1)
            f.write('Info#' + name.text + '#\n')
            i+=1
        except:
            break
    f.close()
    driver.quit()

def main():
    f=pd.read_csv(r'C:/Users/Zhiyan/Desktop/location2.csv')
    url_list=list(f['location'].values)
    address_list=list(f['Address'].values)
    ID=list(f['ID'].values)
    print(len(url_list))
    path1=r'C:/Users/Zhiyan/Desktop/Chargepoint/Crawl_record/'
    counter=0
    time_A=time.time()
    #for i in range(len(url_list)):
    for i in range(10):
        crawl_one_location(url_list[i],path1,ID[i],address_list[i],counter)
        counter+=1
    time_B=time.time()
    Time=round((time_B-time_A)/3600,2)
    send_email(counter,Time)
    print((time_B-time_A)/60)

def send_email(counter,time):
    port=465
    smtp_server='smtp.gmail.com'
    sender_email='yizhiyan1992@gmail.com'
    receiver_email='yizhiyan1992@gmail.com'
    password='Yizhiyan1'
    message='Total number of files '+str(counter)+', working hours '+str(time)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
        server.login(sender_email,password)
        server.sendmail(sender_email,receiver_email,message)

if __name__=='__main__':
    main()
