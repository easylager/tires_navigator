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


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}
HOST = 'https://koleso.av.by'
url = 'https://koleso.av.by/tires/car/season_winter/state_used/city_minsk?tires_count%5B0%5D=4&page=2'
local_id = 1
try:
    with open('av_by_parser_test.json', encoding='utf-8') as file:
         data_list = json.load(file)
except:
    data_list = {}
def pagination():
    url = 'https://koleso.av.by/tires/car/season_winter/state_used/region_minsk?tires_count%5B0%5D=4&page=2'
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')
    pagination = soup.find('li', class_='pages-arrows-index').text.strip().split(' ')[-1]
    return int(pagination)

async def get_data(session, page):
    global local_id
    url = f'https://koleso.av.by/tires/car/season_winter/state_used/region_minsk?tires_count%5B0%5D=4&page={page}'
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    cards = soup.find_all('div', class_='tyre-listing-item')
    for card in cards:
        card_link = card.find('div', class_='tyre-listing-about').find('a').get('href')
        id = card_link.split('/')[-1][-8:]
        if id in data_list:
            print('already exist')
        else:
            async with session.get(url=card_link, headers=headers) as response:
                res = await response.text()
                card_soup = BeautifulSoup(res, 'lxml')
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


                lis = card_soup.find('div', class_='card-info').find_all('li')
                for li in lis:
                    if li.find('dt').text.strip() == 'Посадочный диаметр':
                        diameter = li.find('dd').text.strip()

                    if li.find('dt').text.strip() == 'Ширина профиля, мм':
                        width = li.find('dd').text.strip()

                    if li.find('dt').text.strip() == 'Высота профиля, %':
                        height = li.find('dd').text.strip()



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

                data_list[id] = {
                    'local_id': f'a{local_id}',
                    'Производитель': production,
                    'Модель': model,
                    'Год': year,
                    'Цена': int(price),
                    'Описание': description,
                    'Cсылка': card_link,
                    'Телефон': phone_number,
                    'Остаток протектора': residual_tread_list,
                    'Размер': { 'Ширина': float(width), 'Высота': float(height), 'Диаметр': float(diameter.replace('`', ''))},
                    'Дата публикации': publication_date
                }

                print(f'[INFO] parsed {local_id}')
                local_id += 1





async def gather_data():
    async with aiohttp.ClientSession() as session:
        url = 'https://koleso.av.by/tires/car/season_winter/state_used/region_minsk?tires_count%5B0%5D=4&page=2'
        async with session.get(url, headers=headers) as response:
            res = await response.text()
            soup = BeautifulSoup(res, 'lxml')
            pagination = int(soup.find('li', class_='pages-arrows-index').text.strip().split(' ')[-1])
            tasks = []
            for page in range(1, pagination + 1):
                task = asyncio.create_task(get_data(session, page))
                tasks.append(task)
            await asyncio.gather(*tasks)




def main():
    start = datetime.datetime.now()
    asyncio.run(gather_data())
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y')
    with open(f'av_by_parser_test.json', 'w', encoding='utf-8') as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)
    with open('av_by_parser_test.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for key, value in data_list.items():
            writer.writerow([key, value])
    with open('av_by_parser_test.csv', 'r') as csv_file:
        reader = csv.reader(file)
        mydict = dict(reader)
    print(mydict)
    long = datetime.datetime.now() - start
    print(long)
    print('data_list')

if __name__ == '__main__':
    main()