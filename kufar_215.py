import requests
from bs4 import BeautifulSoup
import json

from time import sleep

from random import choice


HOST = 'http://auto.kufar.by'

urls = ['https://auto.kufar.by/l/r~minsk/cartyres-r16?catihe=v.or:8&catiwi=v.or:11&trq=v.or:15&cnd=1&cative=v.or:1&cur=BYR', 'https://auto.kufar.by/l/r~minsk/cartyres-r16?catihe=v.or:8,9&cur=BYR&cative=v.or:1&catiwi=v.or:11&cnd=1&trq=v.or:15']
def get_data():
    useragents = open('../config/useragents').read().split('\n')
    proxies = open('../config/proxies').read().split('\n')
    try:
        with open('kufar_215', 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
    except:
        data_dict = {}
    new_cards = {}
    pages = urls
    num = 1
    for page in pages:
        headers = {
            'user-agent': choice(useragents)
        }
        proxy = {'http': f'http//{choice(proxies)}'}
        res = requests.get(page, headers=headers, proxies=proxy)
        soup = BeautifulSoup(res.text, 'lxml')
        items = soup.find_all('article')
        print(len(items))
        for item in items[1:]:
            print(item)
            link = item.find('a', class_="kf-UHTj-492ab").get('href')
            id = link.split('/')[-1]
            if id in data_dict:
                continue
            else:
                try:
                    res = requests.get(link, headers=headers)

                except Exception:
                    print('reserror')
                try:
                    card_soup = BeautifulSoup(res.text, 'lxml')

                except Exception:
                    print('no soup')
                try:
                    production = card_soup.find_all('div', class_='kf-Ss-a05aa kf-CoP-e4673 kf-CSh-aa347')[-2].find('div', class_='kf-SV-a2118').text.strip()
                except Exception:
                    production = None
                try:
                    price = card_soup.find('span', class_='kf-qn-8eeb5').text.strip().replace(' р.', '').replace(',', '.').replace(' ', '')
                except Exception:
                    price = None



                data_dict[id] = {
                    'id': f'k{num}',
                    'Производитель': production,
                    'Модель': None,
                    'Год': None,
                    'Цена': price,
                    'Описание': None,
                    'Cсылка': link,

                    #'Размер': {'Высота': height, 'Ширина': width, 'Диаметр': diameter}
                }
                new_cards[id] = {
                    'id': f'k{num}',
                    'Производитель': production,
                    'Модель': None,
                    'Год': None,
                    'Цена': price,
                    'Описание': None,
                    'Cсылка': link,

                    #'Размер': {'Высота': height, 'Ширина': width, 'Диаметр': diameter}
                }
                print(f'[INFO] parsed {num}')
                num += 1
    return new_cards, data_dict




def main():
    #test_parse()
    new_cards, data_dict = get_data()
    with open('kufar_215.json', 'w') as file:
        json.dump(data_dict, file, indent=4, ensure_ascii=False)
    return new_cards

