from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
from selenium.webdriver.common.by import By
from kafka import KafkaProducer
from json import dumps

topic_name = 'testTopic1'
producer = KafkaProducer(bootstrap_servers='172.17.0.1:29092', value_serializer=lambda x: dumps(x).encode('utf-8'))

# Options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")

import re
#text_after = re.sub(regex_search_term, regex_replacement, text_before)
def convert(value):
    value = re.sub(r'\D', "",value)
    return int(value)

product_links = []
url = 'https://www.dienmayxanh.com/laptop#c=44&o=9&pi=10'

browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
browser.implicitly_wait(3) # seconds
browser.get(url)

links = browser.find_elements(By.XPATH, '//*[@class="main-contain"]')  # Vị trí chứa đường dẫn sản phẩm
for i in links:
    link = i.get_attribute("href")   # Lấy đường dẫn và thêm vào list
    product_links.append(link)

count = 0

for link in product_links:
    try:
        browser.get(link)
        product_id = browser.find_element(By.XPATH, '/html/body/section[1]').get_attribute("data-id")
        product = browser.find_element(By.XPATH, '/html/body/section[1]/h1').text
        brand = browser.find_element(By.XPATH, '/html/body/section[1]/ul/li[2]/a').text
        brand = re.sub(r'Laptop ','',brand)
        price = ''
        try:
            price = browser.find_element(By.XPATH, '/html/body/section[1]/div[3]/div[2]/div[1]/div[2]/div/p[1]').text
            price = re.sub(r'\D', "",price)
        except:
            pass
        
        try:
            price = browser.find_element(By.XPATH, '/html/body/section[1]/div[3]/div[2]/div[1]/div[1]/div/strong').text
            price = re.sub(r'\D', "",price)
        except:
            pass

        try:
            price = browser.find_element(By.XPATH, '/html/body/section[1]/div[3]/div[2]/div[2]/div[2]/div/p').text
            price = re.sub(r'\D', "",price)
        except:
            pass

        try:
            price = browser.find_element(By.XPATH, '/html/body/section[1]/div[3]/div[2]/div[3]/div[2]/div/p').text
            price = re.sub(r'\D', "",price)
        except:
            pass

        shop = 'Dienmayxanh'
        url = 'https://www.dienmayxanh.com/Product/GetGalleryItemInPopup?productId=' + product_id +'&isAppliance=false&galleryType=5'
        browser.get(url)
        ram = browser.find_element(By.XPATH, '/html/body/div/div/div[2]/ul/li[1]/div[2]/a').text
        ram = convert(ram)
        scr = browser.find_element(By.XPATH, '/html/body/div/div/div[3]/ul/li[1]/div[2]/span').text
        scr = re.sub(r' \D*', '', scr)
        try:
            capacity = browser.find_element(By.XPATH, '/html/body/div/div/div[2]/ul/li[5]/div[2]/a').text
        except:
            pass
        try:
            capacity = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/ul/li[5]/div[2]/a').text
        except:
            pass

        try:
            capacity = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/ul/li[5]/div[2]/p[1]/a').text
        except:
            pass

        try:
            capacity = browser.find_element(By.XPATH, '/html/body/div/div/div[2]/ul/li[5]/div[2]/span[1]').text
        except:
            pass

        drive_type = 'SSD'
        try:
            core = browser.find_element(By.XPATH, '/html/body/div/div/div[1]/ul/li[1]/div[2]/span/a').text
        except:
            pass

        try:
            core = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/ul/li[1]/div[2]/span/a[1]').text
        except:
            pass

        weight = re.sub(r'(?:Dài.* - Rộng.*Nặng )',"",browser.find_element(By.XPATH, '/html/body/div/div/div[6]/ul/li[1]/div[2]/span').text)
        weight = re.sub(r'(?: kg)','',weight)
        since = browser.find_element(By.XPATH, '/html/body/div/div/div[7]/ul/li[3]/div[2]/span').text
        graphic_card = browser.find_element(By.XPATH, '/html/body/div/div/div[4]/ul/li[1]/div[2]/span').text
        try:
            opsys = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[7]/ul/li[2]/div[2]/a').text
        except:
            pass

        try:
            opsys = browser.find_element(By.XPATH, '/html/body/div/div/div[7]/ul/li[2]/div[2]/a').text
        except:
            pass

        try:
            opsys = browser.find_element(By.XPATH, '/html/body/div/div/div[7]/ul/li[2]/div[2]/span').text
        except:
            pass

        data = {
                "Product" : product,
                "Price" : price,
                "Brand" : brand,
                "Core" : core,
                "RAM" : ram,
                "ScrSize" : scr,
                "GraphicCard" : graphic_card,
                "Drive_Type" : drive_type,
                "Capacity" : capacity,
                "OperSystem" : opsys,
                "Weight" : weight,
                "Madein" : "",
                "Since" : since,
                "Shop": 'Dienmayxanh',
                "URL":link,
                }
        if count == 2:
            break
        else:
            producer.send(topic_name, value=data)
            count += 1
    except:
        pass

browser.close()