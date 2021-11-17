from selenium import webdriver
from selenium.webdriver.common.by import By

import time

from urllib.request import urlopen
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError
import json
import pandas as pd


# 네이버 Geocoding 주소 -> 위도, 경도 변환
client_id = "hf5ccfmn6x"
client_secret = "8bP0prwoBiCj031acT5Z6qWAnANNokIMilIPxV7d"

def address_geocoding(address):
    api_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='
    url = api_url + parse.quote(address)
    request = Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    try:
        response = urlopen(request)
    except HTTPError as e:
        print('HTTP Error!')
        latitude = None
        longitude = None
    else:
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            response_body = json.loads(response_body)  # json
            if response_body['addresses'] == []:
                print("'result' not exist!")
                latitude = None
                longitude = None
            else:
                latitude = response_body['addresses'][0]['y']
                longitude = response_body['addresses'][0]['x']
                print("Success!", latitude, longitude)
        else:
            print('Response error code : %d' % rescode)
            latitude = None
            longitude = None

    return latitude, longitude


# 플레이스 내부 크롤링
def naver_place_crawling(sid):
    driver.get("https://m.map.naver.com/search2/site.naver?code="+sid)

    time.sleep(4)
    reply = driver.find_elements(By.XPATH, '//*[@id="_baseInfoTab"]/div/div')

    results = []

    opening_time = reply.find_element(By.CSS_SELECTOR, 'ul.end_list_basic._dotdotdot._ul_list._no_ellipsis').text
    access_guide = reply.find_element(By.CSS_SELECTOR, 'ul.end_list_option').text
    website = reply.find_elements(By.CSS_SELECTOR, 'div > div:nth-child(1) > div > a')[0].text
    blog_reviews = reply.find_elements(By.XPATH, '//*[@id="_visitsCard"]/div/div/ul/li')
    print(len(blog_reviews))

    blog_results = []
    for index, review in enumerate(blog_reviews):
        # link = review.find_element_by_link_text('a')
        title = review.find_element(By.CSS_SELECTOR, 'h6').text
        content = review.find_element(By.CSS_SELECTOR, 'p').text
        blog_results.append((title, content))

    results.append((opening_time, access_guide, website, blog_results))
    return results


driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get("https://m.map.naver.com/search2/search.naver?query=강아지유치원")
time.sleep(4)
replys = driver.find_elements(By.XPATH, '//*[@id="ct"]/div[2]/ul/li')
print(len(replys))

results = []
for index, reply in enumerate(replys):
    sid = reply.get_attribute('data-sid')
    name = reply.find_element(By.CSS_SELECTOR, 'div.item_tit').text
    address = reply.find_element(By.CSS_SELECTOR, 'div.wrap_item').text.split('\n')[1]
    tel = reply.get_attribute('data-tel')
    latitude, longitude = address_geocoding(address)
    results.append((sid, name, address, tel, latitude, longitude))


print(results)
# 파일 변환 후 저장
data_frame = pd.DataFrame(results, columns=["sid", "name", "address", "tel", "latitude", "longitude"])
print(data_frame)
data_frame.to_csv("results.csv", mode='w')
driver.close()
