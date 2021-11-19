import requests
from bs4 import BeautifulSoup

url = 'https://bamper.by/shiny/detail_span_kleber_krisalp_hp2_205_55_r16_span_4_sht_zimnie_legkovye_b_u_1710_g_v-45990_469566/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')
info_ul = soup.find('span', class_='date').text.strip()
print(info_ul)




