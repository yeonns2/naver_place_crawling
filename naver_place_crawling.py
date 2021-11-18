from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import time
import csv


f = open('results.csv','r')
r = csv.reader(f)
data =[]
for row in r:
        data.append(row[1])

del data[0]
del data[0]
f.close()
print(data)

f = open('info_result.csv','w')
w = csv.writer(f)
driver = webdriver.Chrome(executable_path="./chromedriver")

w.writerow(['sid','opening_time','access_guide','website'])
for sid in data:
        driver.get("https://m.map.naver.com/search2/site.naver?code=" + sid)
        time.sleep(4)
        reply = driver.find_element(By.XPATH, '//*[@id="_baseInfoTab"]/div')
        results = []

        try:
                if (reply.find_element(By.CSS_SELECTOR, 'h5:nth-child(1)').text == '이용시간'):

                        try:
                                opening_time = reply.find_element(By.CSS_SELECTOR,
                                                                  'div > ul.end_list_basic._dotdotdot._ul_list._no_ellipsis').text
                        except:
                                opening_time = ""

                        try:
                                access_guide = reply.find_element(By.CSS_SELECTOR, 'div > ul.end_list_option').text
                        except:
                                access_guide =""
                        try:
                                website = reply.find_elements(By.CSS_SELECTOR, 'div > div._dotdotdot._no_ellipsis')[0].text
                        except:
                                website=""
                        results.append((sid, opening_time, access_guide, website))
                        w.writerow((sid, opening_time, access_guide, website))
                        print(sid, opening_time, access_guide, website)

                elif (reply.find_element(By.CSS_SELECTOR, 'div > h5:nth-child(3)').text == '이용시간'):
                        try:
                                opening_time = reply.find_element(By.CSS_SELECTOR, 'div > ul:nth-child(4)').text
                        except:
                                opening_time = ""
                        try:
                                access_guide = reply.find_element(By.CSS_SELECTOR, 'div > ul.end_list_option').text
                        except:
                                access_guide = ""
                        try:
                                website = reply.find_elements(By.CSS_SELECTOR, 'div > div._dotdotdot._no_ellipsis')[0].text
                        except:
                                website = ""
                        results.append((sid, opening_time, access_guide, website))
                        w.writerow((sid, opening_time, access_guide, website))
                        print(sid, opening_time, access_guide, website)
                elif (reply.find_element(By.CSS_SELECTOR, 'div > h5:nth-child(4)').text == '이용시간'):
                        try:
                                opening_time = reply.find_element(By.CSS_SELECTOR, 'div > ul:nth-child(5)').text
                        except:
                                opening_time = ""
                        try:
                                access_guide = reply.find_element(By.CSS_SELECTOR, 'div > ul.end_list_option').text
                        except:
                                access_guide = ""
                        try:
                                website = reply.find_elements(By.CSS_SELECTOR, 'div > div._dotdotdot._no_ellipsis')[0].text
                        except:
                                website = ""
                        results.append((sid, opening_time, access_guide, website))
                        w.writerow((sid, opening_time, access_guide, website))
                        print(sid, opening_time, access_guide, website)
        except:
                w.writerow((sid, "", "", ""))



driver.close()
