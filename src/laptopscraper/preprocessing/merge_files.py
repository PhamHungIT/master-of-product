import os.path
import os
import io

raw_data_files = ['../data/raw/dmx.final.csv', '../data/raw/fpt.final.csv', '../data/raw/phongvu.final.csv']
columns_line = 'Product,Price,Brand,Core,RAM,ScrSize,GraphicCard,Drive_Type,Capacity,OperSystem,Weight,Madein,Since,Shop,URL'

for i in range(len(raw_data_files)):
    raw_data_files[i] = os.path.dirname(__file__) + '/' + raw_data_files[i]

with io.open(os.path.dirname(__file__) + '/../data/raw/data.csv', 'a', encoding='utf8') as f:
    for file in raw_data_files:
        with io.open(file, 'r', encoding='utf8') as f2:
            for line in f2.readlines():
                if line.strip() == columns_line and os.stat(os.path.dirname(__file__) + '/../data/raw/data.csv').st_size != 0:
                    continue
                else:
                    f.write(line)
                    