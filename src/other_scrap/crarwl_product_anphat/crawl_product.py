import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By

import pandas as pd 

driver = webdriver.Firefox()

#URL
links, title, price, original_price, discount = [],[],[],[],[]
driver.get("https://www.anphatpc.com.vn/may-tinh-xach-tay-laptop.html")
sleep(random.randint(5,10))

# get link/tile/price/oringinal price/discount

# change page
#   /html/body/section/div/div[6]/div[3]/a[1]  preview
#   /html/body/section/div/div[6]/div[3]/a[8] 1->4 && 13 -> 16
#   /html/body/section/div/div[6]/div[3]/a[9] 5->12

count = 1
check_last = 0
shop = []
i = 0
while True:
        print("Crawl Page " + str(count))
        # try:
        
        sleep(random.randint(7,10))
        elems_link = driver.find_elements(By.CSS_SELECTOR , ".p-text .p-name")
        links = [elem_link.get_attribute('href') for elem_link in elems_link] + links

        sleep(random.randint(7,10))
        elems_title = driver.find_elements(By.CSS_SELECTOR , ".p-text .p-name h3")
        title =[elm_text.text for elm_text in elems_title] + title

        sleep(random.randint(7,10))
        elems_price = driver.find_elements(By.CSS_SELECTOR , ".p-text .price-container .p-price")
        price =  [elm_price.text for elm_price in elems_price] + price
        
        sleep(random.randint(7,10))
        elems_original_price = driver.find_elements(By.CSS_SELECTOR , ".p-text .price-container .p-old-price")
        original_price =  [elm_original_price.text for elm_original_price in elems_original_price] + original_price
        
        sleep(random.randint(7,10))
        elems_discount = driver.find_elements(By.CSS_SELECTOR , ".p-text .price-container .p-discount")
        discount = [elm_discount.text for elm_discount in elems_discount] + discount
        
        
        while( i < len(title)):
            shop.append('Anphat computer')
            i +=1 
                   
        sleep(random.randint(7,10))
        
        try:
            try:
                next_pagination = driver.find_element("xpath", "/html/body/section/div/div[6]/div[3]/a[9]")
            except:
                next_pagination = driver.find_element("xpath", "/html/body/section/div/div[6]/font/div/a[9]")
            next_pagination.click()
        except:
            if(count <= 4):
                next_pagination = driver.find_element("xpath", "/html/body/section/div/div[6]/div[3]/a[8]")
                next_pagination.click()
            else:
                if(check_last == 0):
                    next_pagination = driver.find_element("xpath", "/html/body/section/div/div[6]/div[3]/a[6]")
                    next_pagination.click()
                    check_last += 1
                elif(check_last == 1):
                    next_pagination = driver.find_element("xpath", "/html/body/section/div/div[6]/div[3]/a[7]")
                    next_pagination.click()
                    check_last += 1
                
                elif(check_last == 2):
                    next_pagination = driver.find_element("xpath", "/html/body/section/div/div[6]/div[3]/a[8]")
                    next_pagination.click()
                    check_last += 1
                elif(check_last == 3):
                    break
                
        
        count +=1
    
#Close browser
driver.close()    
               
            
    
df1 = pd.DataFrame(list(zip(title, links, price, original_price, discount )), columns=['name', 'price', 'original_price', 'discount', 'shop', 'url' ])  
df1['index'] = np.arange(1, len(df1) +1)
    
#Close browser
driver.close()    
df1.to_csv('laptop_anphatcom.csv', index=False)