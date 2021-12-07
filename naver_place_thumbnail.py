import csv

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

import time
import pandas as pd

f = open('results.csv','r')
r = csv.reader(f)
data =[]
for row in r:
        data.append(row[1])

del data[0]
f.close()
print(data)

f = open('image_result.csv','w')
w = csv.writer(f)
driver = webdriver.Chrome(executable_path="./chromedriver")

w.writerow(['sid','image'])

for sid in data:

        driver.get("https://m.photoviewer.naver.com/map?listUrl=http://m.map.naver.com/search2/site.naver?code="+ sid +"&imgId=0#main/0")
        time.sleep(4)

        try:
                reply = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div/div[1]/div[1]/img')
                image = reply.get_attribute('src')
                print(image)

                w.writerow((sid, image))
                time.sleep(3)
        except NoSuchElementException:
                print('-사진 없음-')
                w.writerow((sid, ""))
                continue
        except ElementNotInteractableException:
                print('-더보기 버튼 모두 클릭 완료-')
                continue

        # while True:
        #         try:
        #                 time.sleep(1)
        #                 reply = driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div/div/div[1]/div[1]/img')
        #                 image = reply.get_attribute('src')
        #                 print(image)
        #                 result = []
        #                 result.append((sid, image))
        #                 w.writerow((sid, image))
        #                 time.sleep(3)
        #
        #                 time.sleep(3)
        #         except NoSuchElementException:
        #                 print('-사진 없음-')
        #                 break
        #         except ElementNotInteractableException:
        #                 print('-더보기 버튼 모두 클릭 완료-')
        #                 break






driver.close()