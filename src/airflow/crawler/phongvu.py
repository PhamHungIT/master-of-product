from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import requests
import csv
import re
from kafka import KafkaProducer
from json import dumps

topic_name = 'testTopic1'
producer = KafkaProducer(bootstrap_servers='172.17.0.1:29092', value_serializer=lambda x: dumps(x).encode('utf-8'))

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}

# Options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")

count = 0

browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
browser.implicitly_wait(10) # seconds
links = ['https://phongvu.vn/apple-scat.01-N004-03?sellerCategoryId=01-N004-03&page=1', 'https://phongvu.vn/apple-scat.01-N004-03?sellerCategoryId=01-N004-03&page=2']
for i in range(1, 11):
    links.append('https://phongvu.vn/laptop-macbook-scat.01-N001?sellerCategoryId=01-N001&page=' + str(i))

product_links = []

for url in links: 
    browser.get(url)
    sleep(3)
    a = browser.find_elements(By.XPATH, '//*[@class="css-pxdb0j"]')  # Vị trí chứa đường dẫn sản phẩm
    for i in a:
        link = i.get_attribute("href")   # Lấy đường dẫn và thêm vào list  
        product_links.append(link)

browser.close()

product_links = list(dict.fromkeys(product_links))

for link in product_links:
    try:
        sku = re.findall('\d+$', link)[0]
        url = 'https://public-setting.tekoapis.com/api/v1/sku-details?sku=' + sku + '&terminalCode=phongvu'
        response = requests.get(url, headers=headers).json()
        data = response.get('data')
        product = data['productInfo']['name']
        product = re.sub('Máy tính xách tay/ ', '', product)
        price = data['prices'][0]['latestPrice']
        brand = data['productInfo']['brand']['name']
        attributes = data['productDetail']['attributeGroups']
        for attribute in attributes:
                if attribute['name'] == 'CPU':
                    core = attribute['value'].strip()
                if attribute['name'] == 'RAM':
                    ram = attribute['value'].strip()
                    if '8GB' in ram:
                        ram = '8'
                    elif '16GB' in ram:
                        ram = '16'
                    elif '32GB' in ram:
                        ram = '32'
                    elif '1 x 4GB' in ram:
                        ram = '4'
                    elif '2 x 4GB' in ram:
                        ram = '8'
                if attribute['name'] == 'Màn hình':
                    scr = attribute['value'].strip()
                    scr = re.findall('(^\d+(\.\d+)*)', scr)[0][0]
                if attribute['name'] == 'Chip đồ họa':
                    graphic_card = attribute['value'].strip()
                if attribute['name'] == 'Lưu trữ':
                    drive_type = 'HDD'
                    drive = attribute['value'].strip()
                    if 'SSD' in drive:
                        drive_type = 'SSD'
                    if '128GB' in drive:
                        capacity = '128'
                    if '256GB' in drive:
                        capacity = '256'
                    if '512GB' in drive:
                        capacity = '512'
                    if '1024GB' in drive:
                        capacity = '1024'
                if attribute['name'] == 'Hệ điều hành':
                    opsys = attribute['value'].strip()
                if attribute['name'] == 'Khối lượng':
                    weight = attribute['value'].strip()
                    weight = re.sub(' kg', '', weight)
        madein = ''
        since = ''

        product_data = dict()
        product_data['Product'] = product
        product_data['Price'] = price
        product_data['Brand'] = brand
        product_data['Core'] = core
        product_data['RAM'] = ram
        product_data['ScrSize'] = scr
        product_data['GraphicCard'] = graphic_card
        product_data['Drive_Type'] = drive_type
        product_data['Capacity'] = capacity
        product_data['OperSystem'] = opsys
        product_data['Weight'] = weight
        product_data['Madein'] = madein
        product_data['Since'] = since
        product_data['Shop'] = 'Phongvu'
        product_data['URL'] = link
        
        if count == 2:
            break
        else:
            producer.send(topic_name, value=product_data)
            count += 1

    except:
        pass