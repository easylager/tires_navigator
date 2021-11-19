import requests
from bs4 import BeautifulSoup
import json
import datetime
import csv
import re
import asyncio
import aiohttp
from aiohttp.client import ClientSession
from time import sleep
import random

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}

HOST = "https://bamper.by/"
try:
    with open('bamper_parser.json', encoding='utf-8') as file:
        data_dict = json.load(file)
except:
    data_dict = {}
SLOW_DOWN = False

l_id = 1
async def get_data(session, page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'accept': '*/*'
    }
    url = f'https://bamper.by/shiny/sezon_zimnie/sostoyanie_bu/tipavto_legkovye/kolvo_4/?ACTION=REWRITED&FORM_DATA=sezon_zimnie%2Fsostoyanie_bu%2Ftipavto_legkovye%2Fkolvo_4&PAGEN_1={page}'
    global l_id
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    cards = soup.find_all('div', class_='item-list')
    for card in cards:
        card_url = HOST + card.find('a').get('href')
        id = card_url.split('/')[-2][-6:]
        if id in data_dict:
            print('already exist')
        else:
            async with session.get(url=card_url, headers=headers) as res:
                res = await res.text()
                card_soup = BeautifulSoup(res, 'lxml')
                try:
                    production = card_soup.find('div', class_='inner inner-box ads-details-wrapper').find('h1', class_='auto-heading').text.split('2')[0].split(' ')[1]
                except Exception:
                    production =None
                try:
                    title = card_soup.find('div', class_='inner inner-box ads-details-wrapper').find('h1', class_='auto-heading').text.strip()
                except Exception:
                    title = None
                try:
                    model = re.split('1|2', title)[0].strip()
                except Exception:
                    model = None
                try:
                    price = card_soup.find('span', class_="auto-price pull-right").text.split('руб')[0].strip()
                    price = price.split()
                    price = ''.join(price)
                    price = int(price) / 100 * 4
                except Exception:
                    price = None
                media_body = card_soup.find('div', class_="key-features").find_all('div', class_='media')
                try:
                    phone_number = card_soup.find('div', class_='user-ads-action').find('a').get('href').split(':')[1]
                except Exception:
                    phone_number = None
                try:
                    production_year = media_body[2].find('span', class_='data-type').text.strip()
                except Exception:
                    production_year = None
                try:
                    size = card_soup.find('span', class_='nobold').text.strip()
                except Exception:
                    size = None
                try:
                    height = size.split('/')[0]
                except Exception:
                    height = None
                try:
                    width = size.split('/')[1].split(' ')[0]
                except Exception:
                    width = None
                try:
                    diameter1 = size.split('R')[1].split(',')[0]
                    diameter = re.sub('\D', '', diameter1)
                except Exception:
                    diameter = None
                if len(production_year) != 4:
                    production_year = None
                try:
                    description = media_body[3].find('span', class_='data-type').text.strip()
                except Exception:
                    description = None
                try:
                    repl_comment = str(description).replace('4 шт', ' ').replace('4 колеса', ' ').replace('5x', '').replace('6x', '').replace('4шт', '')
                    nums = re.findall(r'\d*\.\d+|\d+', repl_comment)
                    residual_tread_list = list(filter(lambda i: float(i) in range(4, 10), nums))
                    if len(residual_tread_list) > 0:
                        residual_tread_list = [int(i) for i in residual_tread_list]
                except:
                    residual_tread_list = None
                try:
                    publication_date = card_soup.find('span', class_='date').text.strip()
                except:
                    publication_date = None

                data_dict[id] = {'id': f'b{l_id}',
                    'Производитель': production,
                    'Модель': model,
                    'Год': production_year,
                    'Цена': price,
                    'Описание': description,
                    'Cсылка': card_url,
                    'Телефон': phone_number,
                    'Остаток протектора': residual_tread_list,
                    'Размер': {'Ширина': float(height), 'Высота': float(width), 'Диаметр': float(diameter)},
                    'Дата публикации': publication_date
                }
                print(f'[INFO] parsed {l_id}')
                l_id += 1
            print(f'[INFO] обработана {page} страница')




async def gather_data():
    async with aiohttp.ClientSession() as session:
        url = 'https://bamper.by/shiny/sezon_zimnie/sostoyanie_bu/tipavto_legkovye/kolvo_4/?ACTION=REWRITED&FORM_DATA=sezon_zimnie%2Fsostoyanie_bu%2Ftipavto_legkovye%2Fkolvo_4&PAGEN_1=100'
        async with session.get(url, headers=headers) as response:
            res = await response.text()
            soup = BeautifulSoup(res, 'lxml')
            pagination = int(soup.find('ul', class_='pagination').find_all('li')[-1].text.strip())
        tasks = []
        for page in range(1, pagination + 1):
            task = asyncio.create_task(get_data(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)



def main():
    start = datetime.datetime.now()
    asyncio.run(gather_data())
    end = datetime.datetime.now() - start
    print(end)
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y')
    with open('bamper_parser.json', 'w', encoding='utf-8') as file:
        json.dump(data_dict, file, indent=4, ensure_ascii=False)
    with open('bamper.csv', 'w') as file:
        writer = csv.writer(file)
        for key, value in data_dict.items():
            writer.writerow([key, value])
    end = datetime.datetime.now() - start
    print(end)




if __name__ == '__main__':
    main()

