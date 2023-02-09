import io
import os.path

raw_data_files = ['../data/raw/dmx.csv', '../data/raw/fpt.csv', '../data/raw/phongvu.csv']

for file in raw_data_files:
    final_file = file[:-3] + 'final.csv'
    with io.open(os.path.dirname(__file__) + '/' + file, 'r', encoding='utf8') as f1, io.open(os.path.dirname(__file__) + '/'  + final_file, 'w', encoding='utf8') as f2:
        for line in f1.readlines():
            if line.strip() == '':
                continue
            f2.write(line)