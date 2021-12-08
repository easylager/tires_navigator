
import requests
from bs4 import BeautifulSoup
import json
import csv
import re
import datetime
import time
from aiohttp.client import ClientSession
import asyncio
import aiohttp
import nest_asyncio
from random import choice


HOST = 'https://koleso.av.by'
urls = ['https://koleso.av.by/tires/car/d_R16/width_215/height_65/state_used/region_minsk?tires_count%5B0%5D=4', 'https://koleso.av.by/tires/car/d_R16/width_215/height_60/state_used/region_minsk?tires_count%5B0%5D=4']




def get_data():
    try:
        with open('../av_215.json', 'r', encoding='utf-8') as file:
            data_list = json.load(file)
    except:
        data_list = {}
    useragents = open('../config/useragents').read().split('\n')
    proxies = open('../config/proxies').read().split('\n')

    new_cards = {}
    local_id = 1
    urls = ['https://koleso.av.by/tires/car/d_R16/width_215/height_65/state_used/region_minsk?tires_count%5B0%5D=4',
            'https://koleso.av.by/tires/car/d_R16/width_215/height_60/state_used/region_minsk?tires_count%5B0%5D=4',
            'https://koleso.av.by/tires/car/d_R15/width_195/height_65/state_used/region_minsk?tires_count%5B0%5D=4']

    for url in urls:
        headers = {
            'user-agent': choice(useragents)
        }
        proxy = {'http': f'http//{choice(proxies)}'}
        res = requests.get(url, headers=headers, proxies=proxy)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        cards = soup.find_all('div', class_='tyre-listing-item')
        for card in cards:
            card_link = card.find('div', class_='tyre-listing-about').find('a').get('href')
            id = card_link.split('/')[-1][-8:]
            if id in data_list:
                #print('already exist')
                continue
            else:
                res = requests.get(card_link, headers=headers, proxies=proxy)
                card_soup = BeautifulSoup(res.text, 'lxml')
                try:
                    production = card_soup.find_all("li", class_="breadcrumb-item breadcrumb-back")[-1].find('a', class_='breadcrumb-link').text.strip()
                except Exception:
                    production = 'not found'
                try:
                    model1 = card_soup.find('h1', class_='card-title').text.strip()
                    model = re.split('2|1', model1)[0].replace(' N/A', '').replace('Германия', '').strip()
                except Exception:
                    model = 'not found'


                try:
                    price = card.find('h5').text.strip().split(' ')[0]
                except Exception:
                    price = 'not found'


                try:
                    card_li1 = card_soup.find('div', class_='card-info').find_all('li')[-1].find('dt').text.strip()
                    if card_li1 == 'Год производства':
                        year = int(card_soup.find('div', class_='card-info').find_all('li')[-1].find('dd').text.strip())
                    else:
                        year = 'no year'
                except Exception:
                    year = 'year not found'

                try:
                    description = card_soup.find('div', class_='card-description js-card-description').find('p').text.strip()
                except Exception:
                    description = 'not found'

                try:
                    repl_comment = str(description).replace('4 шт', ' ').replace('4 колеса', ' ').replace('5x', '').replace('6x', '').replace('4шт', '')
                    nums = re.findall(r'\d*\.\d+|\d+', repl_comment)
                    residual_tread_list = list(filter(lambda i: float(i) in range(4, 10), nums))
                    if len(residual_tread_list) > 0:
                        residual_tread_list = [int(i) for i in residual_tread_list]
                except:
                    residual_tread_list = None


                try:
                    phone_number = card_soup.find('div', class_='card-contacts-phones').find('a', class_='card-contacts-phones-button js-get-phone').get('href').replace('tel:', '')
                except Exception:
                    phone_number = 'not found'
                try:
                    publication_date = card_soup.find('ul', class_="card-about").find('li', class_='card-about-item card-about-item-dates').find('dd').text.strip()
                except Exception:
                    publication_date = None
                try:
                    updata_data = card_soup.find('ul', class_="card-about").find('li', class_='card-about-item card-about-item-dates').find_all('dd')[1].text.strip()
                except:
                    updata_data = ''
                data_list[id] = {
                    'local_id': f'a{local_id}',
                    'Производитель': production,
                    'Модель': model,
                    'Год': year,
                    'Цена': price,
                    'Описание': description,
                    'Cсылка': card_link,
                    'Телефон': phone_number,
                    'Остаток протектора': residual_tread_list,
                    #'Размер': { 'Ширина': float(width), 'Высота': float(height), 'Диаметр': float(diameter.replace('`', ''))},
                    'Дата публикации': publication_date,
                    'Дата продвижения': updata_data
                }
                new_cards[id] = {
                    'local_id': f'a{local_id}',
                    'Производитель': production,
                    'Модель': model,
                    'Год': year,
                    'Цена': price,
                    'Описание': description,
                    'Cсылка': card_link,
                    'Телефон': phone_number,
                    'Остаток протектора': residual_tread_list,
                    #'Размер': {'Ширина': float(width), 'Высота': float(height),
                               #'Диаметр': float(diameter.replace('`', ''))},
                    'Дата публикации': publication_date,
                    'Дата продвижения': updata_data
                }

                print(f'[INFO] parsed {local_id}')
                local_id += 1
    return new_cards, data_list


def main():
    new_cards, data_list = get_data()
    with open('../av_215.json', 'w', encoding='utf-8') as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)
    return new_cards

