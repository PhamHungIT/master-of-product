import pandas as pd
import json
import os

laptops = []

df = pd.read_csv(os.path.dirname(__file__) + '/../data/clean/data.csv')

gpus = {
    'Intel Iris Xe': {
        'brand': 'Intel',
        'discrete': False,
        'raw_name': 'Intel Iris Xe',
        'model': 'Iris',
        'model_power': 1,
        'name': 'Intel Iris Xe'
    },
    'Intel UHD 620': {
        'brand': 'Intel',
        'discrete': False,
        'raw_name': 'Intel UHD Graphics 620',
        'model': 'UHD',
        'model_power': 1,
        'model_number': '620',
        'name': 'Intel UHD 620'
    },
    'Intel HD 620': {
        'brand': 'Intel',
        'discrete': False,
        'raw_name': 'Intel UHD Graphics 620',
        'model': 'UHD',
        'model_power': 0,
        'model_number': '620',
        'name': 'Intel UHD 620'
    },
    'Intel HD 520': {
        'brand': 'Intel',
        'discrete': False,
        'raw_name': 'Intel UHD Graphics 520',
        'model': 'UHD',
        'model_power': 0,
        'model_number': '520',
        'name': 'Intel UHD 520'
    },
    'Apple M2 GPU': {
        'brand': 'Apple',
        'discrete': True,
        'raw_name': 'Apple M2 GPU',
        'model': 'M2',
        'model_power': 4,
        'model_number': '2',
        "memory_gbs": 8,
        'name': 'Apple M2 GPU'
    },
    'Apple M1 GPU': {
        'brand': 'Apple',
        'discrete': True,
        'raw_name': 'Apple M1 GPU',
        'model': 'M1',
        'model_power': 4,
        'model_number': '1',
        "memory_gbs": 6,
        'name': 'Apple M1 GPU'
    },
    'Radeon Vega': {
        'brand': 'Radeon',
        'discrete': True,
        'raw_name': 'Radeon Vega Graphics',
        'model': 'Vega',
        'model_power': 0,
        'name': 'Radeon Vega'
    },
    'Quadro T500 (4GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Quadro T500-4GB',
        'model': 'Quadro',
        'model_power': 3,
        'model_number': '500',
        "memory_gbs": 4,
        'name': 'Quadro T500 (4GB)'
    },
    'GeForce RTX3070 (8GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce 3070RTX-8GB',
        'model': 'RTX',
        'model_power': 4,
        'model_number': '3070',
        "memory_gbs": 8,
        'name': 'GeForce RTX3070 (8GB)'
    },
    'GeForce RTX3060 (6GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce 3060RTX-6GB',
        'model': 'RTX',
        'model_power': 4,
        'model_number': '3060',
        "memory_gbs": 6,
        'name': 'GeForce RTX3060 (6GB)'
    },
    'GeForce RTX3050Ti (4GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce RTX3050 Ti-4GB',
        'model': 'RTX',
        'model_power': 3,
        'model_number': '3050',
        "memory_gbs": 4,
        'name': 'GeForce RTX3050Ti (4GB)'
    },
    'GeForce RTX3050 (4GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce 3050RTX-4GB',
        'model': 'RTX',
        'model_power': 3,
        'model_number': '3050',
        "memory_gbs": 4,
        'name': 'GeForce RTX3050 (4GB)'
    },
    'GeForce RTX1650 (4GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce 1650RTX-4GB',
        'model': 'RTX',
        'model_power': 3,
        'model_number': '1650',
        "memory_gbs": 4,
        'name': 'GeForce RTX1650 (4GB)'
    },
    'GeForce GTX1650 (4GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce 1650GTX-4GB',
        'model': 'GTX',
        'model_power': 3,
        'model_number': '1650',
        "memory_gbs": 4,
        'name': 'GeForce GTX1650 (4GB)'
    },
    'GeForce MX570 (2GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce 570MX-2GB',
        'model': 'MX',
        'model_power': 2,
        'model_number': '570',
        "memory_gbs": 2,
        'name': 'GeForce MX570 (2GB)'
    },
    'GeForce MX550 (2GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce 550MX-2GB',
        'model': 'MX',
        'model_power': 2,
        'model_number': '550',
        "memory_gbs": 2,
        'name': 'GeForce MX550 (2GB)'
    },
    'GeForce MX450 (2GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce 450MX-2GB',
        'model': 'MX',
        'model_power': 2,
        'model_number': '450',
        "memory_gbs": 2,
        'name': 'GeForce MX450 (2GB)'
    },
    'GeForce MX350 (2GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce 350MX-2GB',
        'model': 'MX',
        'model_power': 2,
        'model_number': '350',
        "memory_gbs": 2,
        'name': 'GeForce MX350 (2GB)'
    },
    'GeForce MX330 (2GB)': {
        'brand': 'GeForce',
        'discrete': True,
        'raw_name': 'Geforce 330MX-2GB',
        'model': 'MX',
        'model_power': 2,
        'model_number': '330',
        "memory_gbs": 2,
        'name': 'GeForce MX330 (2GB)'
    }
}

for i, row in df.iterrows():
    specs = {}
    specs['name'] = df.at[i, 'name']
    specs['brand'] = df.at[i, 'brand']
    specs['cpu'] = str(df.at[i, 'cpu'])
    specs['ram_gbs'] = str(df.at[i, 'ram'])
    storage = [{'hdd_gbs': str(df.at[i, 'memory']), 'is_ssd': True}]
    specs['storage'] = storage
    specs['screen_size_inches'] = str(df.at[i, 'scrsize'])
    specs['graphics_card'] = gpus[df.at[i, 'gpu']]
    specs['weight_kgs'] = str(df.at[i, 'weight'])
    specs['price'] = str(round(int(df.at[i,'price'])/1000, 2))
    specs['url'] = df.at[i, 'url']
    laptops.append(specs)

jsonString = json.dumps(laptops, indent=4)
jsonFile = open(os.path.dirname(__file__) + '/../data/json/laptops.json', "w")
jsonFile.write(jsonString)
jsonFile.close()