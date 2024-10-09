import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import math
from dataframe import *

pd.set_option("display.max_columns", None)
pd.options.display.expand_frame_repr = False
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

# req = requests.get("https://www.muiv.ru/sveden/education/oop/")
# src = req.text
# # инициализируем html-код страницы
# soup = BeautifulSoup(src, 'html.parser')
# # for link in soup.find_all('td', itemprop= 'eduName'):
# table = soup.find('table')
# table_rows = table.find_all('tr')
# data = []
# for tr in table_rows:
#     td = tr.find_all('td')
#     row = [tr.text for tr in td]
#     data.append(row)
# df = pd.DataFrame(data, columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'])
# df = df.drop(columns=['A', 'E', 'F', 'H', 'I', 'J', 'K'])
# df.drop(0, inplace=True)
# for x in range(len(df)):
#     print(df[x, 2])
#     split = df[x, 3]
#     slit1 = split1.split(",")
#     df[x, 3] = split1[2]



def raspisanieparser():
    req = requests.get("https://www.muiv.ru/studentu/fakultet-it/raspisaniya/")
    # считываем текст HTML-документа
    src = req.text
    # инициализируем html-код страницы
    soup = BeautifulSoup(src, 'lxml')
    for link in soup.find_all('a', class_= 'download__src')[2:2]:
        url = "https://www.muiv.ru" + link.get('href')
        response = requests.get(url, headers=headers, stream=True)
        file_Path = 'Modules/1.xlsx'

        if response.status_code == 200:
            with open(file_Path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=None):
                    file.write(chunk)

                print('File downloaded successfully')
        else:
            print('Failed to download file')

        excelparser()