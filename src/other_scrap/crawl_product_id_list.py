from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}

params = {
    'limit': '40',
    'include': 'advertisement',
    'aggregations': '2',
    'trackity_id': 'e3266e52-cccc-6694-de84-1ec8082cdf8f',
    'category': '8095',
    'page': '1',
    'urlKey': 'laptop'
}

url = 'https://tiki.vn/api/personalish/v1/blocks/listings'

def crawl_product_id():
    product_id_list = []
    i = 1
    while True:
        print('Crawl page:', i)
        params['page'] = i
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            print('Request success.')
            records = response.json().get('data')
            if len(records) == 0:
                break
            for record in records:
                product_id = record.get('id')
                product_id_list.append({'id': product_id})
            i += 1
        else:
            break
    
    return product_id_list, i

def save_product_id_list(product_id_list=[]):
    df = pd.DataFrame(product_id_list)
    df.to_csv('product_id_list.csv', index=False)

product_id_list, no_pages = crawl_product_id()
save_product_id_list(product_id_list)

print('No. Page:', no_pages)
print('No. Product ID:', len(product_id_list))
