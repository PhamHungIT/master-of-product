from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}

url = 'https://tiki.vn/api/v2/products/{}'

def parser_product(json_data):
    product_data = dict()
    product_data['id'] = json_data.get('id')
    product_data['name'] = json_data.get('name')
    product_data['product_url'] = json_data.get('short_url')
    product_data['price'] = json_data.get('price')
    product_data['original_price'] = json_data.get('original_price')
    product_data['discount'] = json_data.get('discount')
    product_data['brand'] = json_data.get('brand').get('name')
    product_data['inventory_status'] = json_data.get('inventory_status')
    product_data['stock_item_quantity'] = json_data.get('stock_item').get('qty')
    product_data['product_category'] = 'laptop'
    return product_data

id_df = pd.read_csv('product_id_list.csv')
product_ids = id_df.id.to_list()
result = []

for product_id in tqdm(product_ids, total=len(product_ids)):
    response = requests.get(url.format(product_id), headers=headers)
    if response.status_code == 200:
        print('Crawl data {} success.'.format(product_id))
        result.append(parser_product(response.json()))

product_df = pd.DataFrame(result)
product_df.to_csv('laptop_tiki.csv', index=False)