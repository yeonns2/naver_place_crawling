from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import csv


f = open('results.csv','r')
r = csv.reader(f)
data =[]
for row in r:
        data.append(row[1])

del data[0]
f.close()
print(data)

f = open('info_result.csv','w')
w = csv.writer(f)
driver = webdriver.Chrome(executable_path="./chromedriver")

w.writerow(['sid','opening_time','access_guide','website'])
for sid in data:

        driver.get("https://m.map.naver.com/search2/site.naver?code="+sid)
        time.sleep(4)
        reply = driver.find_element(By.XPATH, '//*[@id="_baseInfoTab"]/div')

        results = []
        opening_time = reply.find_element(By.XPATH, 'div > ul:nth-child(5)').text
        access_guide = reply.find_element(By.XPATH, '').text
        website = reply.find_elements(By.XPATH,'div/div[2]')[0].text

        results.append((sid, opening_time,access_guide, website))
        w.writerow((sid, opening_time,access_guide, website))
        print(sid,opening_time, access_guide, website)


driver.close()
