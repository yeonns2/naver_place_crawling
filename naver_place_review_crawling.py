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

f = open('review_result.csv','w')
w = csv.writer(f)
driver = webdriver.Chrome(executable_path="./chromedriver")

w.writerow(['sid','link','title','content','date'])
for sid in data:

        driver.get("https://m.map.naver.com/search2/site.naver?code="+ sid + "#/moreInfo/visits")
        time.sleep(4)


        while True:
                try:
                        time.sleep(1)
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                        time.sleep(3)
                        driver.find_element(By.XPATH, '//*[@id="_visitsMoreInfo"]/div[2]/div/div/a').click()
                        time.sleep(3)
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                        time.sleep(3)

                except NoSuchElementException:
                        print('-블로그 리뷰 없음-')
                        break
                except ElementNotInteractableException:
                        print('-더보기 버튼 모두 클릭 완료-')
                        break


        reply = driver.find_element(By.XPATH, '//*[@id="_siteviewTopArea"]/div[1]/div[2]/div[1]/div/a')
        sid = reply.get_attribute('data-cid')
        blog_reviews = reply.find_elements(By.XPATH, '//*[@id="_visitsMoreInfo"]/div[2]/div/div/div[1]/div/ul/li')
        print(len(blog_reviews))
        blog_results =[]
        for index, review in enumerate(blog_reviews):

                link = review.find_element(By.CSS_SELECTOR,'a').get_attribute('data-url')
                title = review.find_element(By.CSS_SELECTOR, 'h6').text
                content = review.find_element(By.CSS_SELECTOR, 'p').text
                date = review.find_element(By.CSS_SELECTOR,'a > div.blog_date').text.replace("블로그","")

                blog_results.append((sid, link, title, content, date))
                w.writerow((sid, link, title, content, date))

driver.close()