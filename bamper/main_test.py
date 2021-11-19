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


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}
HOST = "https://bamper.by/"
data_list = []
urls = [f'https://bamper.by/shiny/sezon_zimnie/sostoyanie_bu/tipavto_legkovye/kolvo_4/?ACTION=REWRITED&FORM_DATA=sezon_zimnie%2Fsostoyanie_bu%2Ftipavto_legkovye%2Fkolvo_4&PAGEN_1={page}' for page in range(1, 5)
]
id = 1


async def fetch(session, url):
    async with session.get(url=url, headers=headers) as response:
        return await response.text(encoding='utf-8')


async def process(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'lxml')
        cards = soup.find_all('div', class_='item-list')
        cards_urls = []
        for card in cards:
            card_url = HOST + card.find('a').get('href')
            cards_urls.append(card_url)
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(get_data(i, session)) for i in cards_urls]
        tasks = asyncio.gather(*tasks)
        loop.run_until_complete(tasks)



async def get_data(url, session):
    global id
    html = await fetch(session, url)
    card_soup = BeautifulSoup(html, 'lxml')
    try:
        production = card_soup.find('div', class_='inner inner-box ads-details-wrapper').find('h1',
                                                                                              class_='auto-heading').text.split(
            '2')[0].split(' ')[1]
    except Exception:
        production = None
    try:
        title = card_soup.find('div', class_='inner inner-box ads-details-wrapper').find('h1',
                                                                                         class_='auto-heading').text.strip()
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
        repl_comment = str(description).replace('4 шт', ' ').replace('4 колеса', ' ').replace('5x', '').replace(
            '6x', '').replace('4шт', '')
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

    data_list.append({
        'id': f'b{id}',
        'Производитель': production,
        'Модель': model,
        'Год': production_year,
        'Цена': price,
        'Описание': description,
        'Cсылка': url,
        'Телефон': phone_number,
        'Остаток протектора': residual_tread_list,
        'Размер': {'Ширина': float(height), 'Высота': float(width), 'Диаметр': float(diameter)},
        'Дата публикации': publication_date
    })
    id += 1
    print(f'[INFO] parsed {id}')


start = datetime.datetime.now()
for i in urls:
    process(i)
with open('bamper_parser.json', 'w', encoding='utf-8') as file:
    json.dump(data_list, file, indent=4, ensure_ascii=False)
with open('bamper_parser.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow((
        'id',
        'Производитель',
        'Модель',
        'Год',
        'Цена',
        'Описание',
        'Cсылка',
        'Телефон',
        'Остаток протектора',
        'Размер',
        'Дата публикации'
    ))

for card in data_list:
    with open('bamper_parser.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            card['id'],
            card['Производитель'],
            card['Модель'],
            card['Год'],
            card['Цена'],
            card['Описание'],
            card['Cсылка'],
            card['Телефон'],
            card['Остаток протектора'],
            card['Размер'],
            card['Дата публикации']
        ))
end = datetime.datetime.now() - start
print(end)

