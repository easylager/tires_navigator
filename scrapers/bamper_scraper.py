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
from random import choice

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}

HOST = "https://bamper.by/"
urls = ['https://bamper.by/shiny/diametr_r16/sezon_zimnie/shirina_215/vysota_60/sostoyanie_bu/tipavto_legkovye/kolvo_4/',
        'https://bamper.by/shiny/diametr_r16/sezon_zimnie/shirina_215/vysota_65/sostoyanie_bu/tipavto_legkovye/kolvo_4/',
        'https://bamper.by/shiny/diametr_r15/sezon_zimnie/shirina_195/vysota_65/sostoyanie_bu/kolvo_4/?ACTION=REWRITED&FORM_DATA=diametr_r15%2Fsezon_zimnie%2Fshirina_195%2Fvysota_65%2Fsostoyanie_bu%2Fkolvo_4&PAGEN_1=2']

SLOW_DOWN = False

l_id = 1
def get_data():
    try:
        with open('../storages/bamper_storage.json', encoding='utf-8') as file:
            data_dict = json.load(file)
    except:
        data_dict = {}
    #useragents = open('../config/useragents').read().split('\n')
    proxies = open('../config/proxies').read().split('\n')
    new_cards = {}
    for url in urls:
        global l_id
        #headers = {
            #'user-agent': choice(useragents),
        #}
        proxy = {'http': f'http://{choice(proxies)}'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        cards = soup.find_all('div', class_='item-list')
        for card in cards:
            card_url = HOST + card.find('a').get('href')
            id = card_url.split('/')[-2][-6:]
            if id in data_dict:
                #print('exist')
                continue
            else:
                print('new')
                res = requests.get(card_url, headers=headers)
                card_soup = BeautifulSoup(res.text, 'lxml')
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
                #try:
                   # height = size.split('/')[0]
                # except Exception:
                   # height = None
                #try:
                    #width = size.split('/')[1].split(' ')[0]
                #except Exception:
                   # width = None
                #try:
                    #diameter1 = size.split('R')[1].split(',')[0]
                    #diameter = re.sub('\D', '', diameter1)
                #except Exception:
                    #diameter = None
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
                    #'Размер': {'Ширина': float(height), 'Высота': float(width), 'Диаметр': float(diameter)},
                    'Дата публикации': publication_date
                }
                new_cards[id] = {'id': f'b{l_id}',
                                 'Производитель': production,
                                 'Модель': model,
                                 'Год': production_year,
                                 'Цена': price,
                                 'Описание': description,
                                 'Cсылка': card_url,
                                 'Телефон': phone_number,
                                 'Остаток протектора': residual_tread_list,
                                 #'Размер': {'Ширина': float(height), 'Высота': float(width),
                                            #'Диаметр': float(diameter)},
                                 'Дата публикации': publication_date
                                 }
                print(f'[INFO] parsed {l_id}')
                l_id += 1
    return new_cards, data_dict




def main():
    new_cards, data_dict = get_data()
    with open('../storages/bamper_storage.json', 'w', encoding='utf-8') as file:
        json.dump(data_dict, file, indent=4, ensure_ascii=False)
    return new_cards




