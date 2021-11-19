import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import datetime
import csv


HOST = "https://bamper.by/"
data_list = []

async def get_page_data(session, page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    url = f'https://bamper.by/shiny/sezon_zimnie/sostoyanie_bu/tipavto_legkovye/kolvo_4/?ACTION=REWRITED&FORM_DATA=sezon_zimnie%2Fsostoyanie_bu%2Ftipavto_legkovye%2Fkolvo_4&PAGEN_1={page}'

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        cards = soup.find_all('div', class_='item-list')
        id = 1
        for card in cards:
            card_url = HOST + card.find('a').get('href')
            r = requests.get(card_url, headers=headers)
            card_soup = BeautifulSoup(r.text, 'lxml')
            try:
                production = card_soup.find('div', class_='inner inner-box ads-details-wrapper').find('h1', class_='auto-heading').text.split('2')[0].split(' ')[1]
            except Exception:
                production = None
            try:
                title = card_soup.find('div', class_='inner inner-box ads-details-wrapper').find('h1', class_='auto-heading').text.split(
                '2')[0]
            except Exception:
                title = None
            try:
                price = card_soup.find('span', class_="auto-price pull-right").text.split('руб')[0].strip()
            except Exception:
                price = None
            try:
                media_body = card_soup.find('div', class_="key-features").find_all('div', class_='media')
            except Exception:
                media_body = None
            try:
                phone_number = card_soup.find('div', class_='user-ads-action').find('a').get('href').split(':')[1]
            except Exception:
                phone_number = None
            try:
                production_year = media_body[2].find('span', class_='data-type').text.strip()
            except:
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
                diameter = size.split('R')[1].split(',')[0]
            except Exception:
                diameter = None
            if len(production_year) != 4:
                production_year = None
            try:
                description = media_body[3].find('span', class_='data-type').text.strip()
            except Exception:
                description = None
            if price:
               price = price.split()
               price = ''.join(price)
            data_list.append({
                'id': f'b{id}',
                'Производитель': production,
                'Модель': title,
                'Год': production_year,
                'Цена': int(price) / 100 * 4,
                'Описание': description,
                'Cсылка': card_url,
                'Телефон': phone_number,
                'Размер': {'Ширина': height, 'Высота': width, 'Диаметр': diameter}
            })
            id += 1
        print(f'[INFO] обрработал страницу {page}')


async def gather_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(1, 6):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)






def main():
    start_time = time.time()
    asyncio.run(gather_data())
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    with open(f'bamper_{cur_time}_async.json', 'w', encoding='utf-8') as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)
    finish_time = time.time() - start_time
    with open(f'bamper_{cur_time}_async.csv', 'w') as file:
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
            'Размер'
        ))
    for card in data_list:
        with open(f'bamper_{cur_time}_async.csv', 'a') as file:
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
                card['Размер']
            ))
    print(f'Затраченое время на работу: {finish_time}')

if __name__ == '__main__':
    main()
